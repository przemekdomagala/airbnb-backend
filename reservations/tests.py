from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from datetime import date, timedelta

from listings.models import Listing
from .models import Reservation, AvailabilityBlock

User = get_user_model()


class ReservationModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.owner = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='ownerpass123'
        )
        self.listing = Listing.objects.create(
            title='Test Listing',
            description='A test listing',
            price_per_night=Decimal('100.00'),
            location='Test City',
            owner=self.owner
        )

    def test_reservation_creation(self):
        """Test creating a reservation"""
        reservation = Reservation.objects.create(
            user=self.user,
            listing=self.listing,
            check_in=date.today() + timedelta(days=1),
            check_out=date.today() + timedelta(days=3),
            guests_adults=2,
            guests_children=0,
            guest_first_name='John',
            guest_last_name='Doe',
            guest_email='john@example.com',
            guest_phone='+1234567890',
            price_per_night=Decimal('100.00'),
            subtotal=Decimal('200.00'),
            taxes_and_fees=Decimal('30.00'),
            total_amount=Decimal('230.00'),
        )
        
        self.assertEqual(reservation.total_nights, 2)
        self.assertTrue(reservation.confirmation_number.startswith('DB'))
        self.assertEqual(reservation.status, 'pending')
        self.assertEqual(reservation.payment_status, 'pending')

    def test_confirmation_number_generation(self):
        """Test that confirmation numbers are unique"""
        reservation1 = Reservation.objects.create(
            user=self.user,
            listing=self.listing,
            check_in=date.today() + timedelta(days=1),
            check_out=date.today() + timedelta(days=2),
            guests_adults=1,
            guest_first_name='Test',
            guest_last_name='User',
            guest_email='test@example.com',
            guest_phone='+1234567890',
            price_per_night=Decimal('100.00'),
            subtotal=Decimal('100.00'),
            taxes_and_fees=Decimal('15.00'),
            total_amount=Decimal('115.00'),
        )
        
        reservation2 = Reservation.objects.create(
            user=self.user,
            listing=self.listing,
            check_in=date.today() + timedelta(days=5),
            check_out=date.today() + timedelta(days=6),
            guests_adults=1,
            guest_first_name='Test',
            guest_last_name='User2',
            guest_email='test2@example.com',
            guest_phone='+1234567891',
            price_per_night=Decimal('100.00'),
            subtotal=Decimal('100.00'),
            taxes_and_fees=Decimal('15.00'),
            total_amount=Decimal('115.00'),
        )
        
        self.assertNotEqual(reservation1.confirmation_number, reservation2.confirmation_number)


class ReservationAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.owner = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='ownerpass123'
        )
        self.listing = Listing.objects.create(
            title='Test Listing',
            description='A test listing',
            price_per_night=Decimal('100.00'),
            location='Test City',
            owner=self.owner
        )
        self.client.force_authenticate(user=self.user)    
    
    def test_create_reservation(self):
        """Test creating a reservation via API"""
        url = reverse('reservations:reservation-list-create')
        data = {
            'listing_id': str(self.listing.id),
            'check_in': str(date.today() + timedelta(days=10)),
            'check_out': str(date.today() + timedelta(days=12)),
            'guests_adults': 2,
            'guests_children': 0,
            'guest_first_name': 'John',
            'guest_last_name': 'Doe',
            'guest_email': 'john@example.com',
            'guest_phone': '+1234567890',
            'special_requests': 'Late check-in',
            'payment_method': 'card'        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check that reservation was created
        reservation = Reservation.objects.get(id=response.data['id'])
        self.assertEqual(reservation.user, self.user)
        self.assertEqual(reservation.listing, self.listing)
        self.assertEqual(reservation.total_nights, 2)

    def test_list_user_reservations(self):
        """Test listing user's reservations"""
        # Create a reservation
        reservation = Reservation.objects.create(
            user=self.user,
            listing=self.listing,
            check_in=date.today() + timedelta(days=1),
            check_out=date.today() + timedelta(days=3),
            guests_adults=2,
            guest_first_name='John',
            guest_last_name='Doe',
            guest_email='john@example.com',
            guest_phone='+1234567890',
            price_per_night=Decimal('100.00'),
            subtotal=Decimal('200.00'),
            taxes_and_fees=Decimal('30.00'),
            total_amount=Decimal('230.00'),
        )
        
        url = reverse('reservations:reservation-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], str(reservation.id))

    def test_get_reservation_detail(self):
        """Test getting reservation details"""
        reservation = Reservation.objects.create(
            user=self.user,
            listing=self.listing,
            check_in=date.today() + timedelta(days=1),
            check_out=date.today() + timedelta(days=3),
            guests_adults=2,
            guest_first_name='John',
            guest_last_name='Doe',
            guest_email='john@example.com',
            guest_phone='+1234567890',
            price_per_night=Decimal('100.00'),
            subtotal=Decimal('200.00'),
            taxes_and_fees=Decimal('30.00'),
            total_amount=Decimal('230.00'),
        )
        
        url = reverse('reservations:reservation-detail', kwargs={'id': reservation.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(reservation.id))
        self.assertEqual(response.data['guest_name'], 'John Doe')

    def test_check_availability(self):
        """Test availability checking"""
        # Create a confirmed reservation
        Reservation.objects.create(
            user=self.user,
            listing=self.listing,
            check_in=date.today() + timedelta(days=5),
            check_out=date.today() + timedelta(days=7),
            guests_adults=2,
            guest_first_name='John',
            guest_last_name='Doe',
            guest_email='john@example.com',
            guest_phone='+1234567890',
            price_per_night=Decimal('100.00'),
            subtotal=Decimal('200.00'),
            taxes_and_fees=Decimal('30.00'),
            total_amount=Decimal('230.00'),
            status='confirmed'
        )
        
        url = reverse('reservations:availability-check')
        
        # Test overlapping dates (should be unavailable)
        data = {
            'listing_id': str(self.listing.id),
            'check_in': str(date.today() + timedelta(days=4)),
            'check_out': str(date.today() + timedelta(days=6))
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['available'])
        
        # Test non-overlapping dates (should be available)
        data = {
            'listing_id': str(self.listing.id),
            'check_in': str(date.today() + timedelta(days=1)),
            'check_out': str(date.today() + timedelta(days=3))
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['available'])

    def test_cancel_reservation(self):
        """Test cancelling a reservation"""
        reservation = Reservation.objects.create(
            user=self.user,
            listing=self.listing,
            check_in=date.today() + timedelta(days=1),
            check_out=date.today() + timedelta(days=3),
            guests_adults=2,
            guest_first_name='John',
            guest_last_name='Doe',
            guest_email='john@example.com',
            guest_phone='+1234567890',
            price_per_night=Decimal('100.00'),
            subtotal=Decimal('200.00'),
            taxes_and_fees=Decimal('30.00'),
            total_amount=Decimal('230.00'),
            status='confirmed'
        )
        
        url = reverse('reservations:reservation-cancel', kwargs={'reservation_id': reservation.id})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that reservation was cancelled
        reservation.refresh_from_db()
        self.assertEqual(reservation.status, 'cancelled')

    def test_booking_step_validation(self):
        """Test the 3-step booking process"""
        # Step 1: Guest information
        url = reverse('reservations:booking-step-1')
        data = {
            'listing_id': str(self.listing.id),
            'check_in': str(date.today() + timedelta(days=1)),
            'check_out': str(date.today() + timedelta(days=3)),
            'guests_adults': 2,
            'guests_children': 0,
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john@example.com',
            'phone': '+1234567890',
            'specialRequests': 'Late check-in'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['valid'])
        
        # Step 2: Payment information
        url = reverse('reservations:booking-step-2')
        data = {
            'payment_method': 'card',
            'card_details': {
                'number': '4242424242424242',
                'expiry': '12/25',
                'cvv': '123',
                'name': 'John Doe'
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['valid'])
        
        # Step 3: Final confirmation
        url = reverse('reservations:booking-step-3')
        full_data = {
            'listing_id': str(self.listing.id),
            'check_in': str(date.today() + timedelta(days=1)),
            'check_out': str(date.today() + timedelta(days=3)),
            'guests_adults': 2,
            'guests_children': 0,
            'guest_first_name': 'John',
            'guest_last_name': 'Doe',
            'guest_email': 'john@example.com',
            'guest_phone': '+1234567890',
            'special_requests': 'Late check-in',
            'payment_method': 'card'
        }
        response = self.client.post(url, full_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])

    def test_landlord_reservations(self):
        """Test landlord viewing reservations for their properties"""
        # Create reservation for the owner's listing
        reservation = Reservation.objects.create(
            user=self.user,
            listing=self.listing,
            check_in=date.today() + timedelta(days=1),
            check_out=date.today() + timedelta(days=3),
            guests_adults=2,
            guest_first_name='John',
            guest_last_name='Doe',
            guest_email='john@example.com',
            guest_phone='+1234567890',
            price_per_night=Decimal('100.00'),
            subtotal=Decimal('200.00'),
            taxes_and_fees=Decimal('30.00'),
            total_amount=Decimal('230.00'),
        )
        
        # Switch to owner account
        self.client.force_authenticate(user=self.owner)
        
        url = reverse('reservations:landlord-reservations')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], str(reservation.id))


class AvailabilityBlockTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.listing = Listing.objects.create(
            title='Test Listing',
            description='A test listing',
            price_per_night=Decimal('100.00'),
            location='Test City',
            owner=self.user
        )

    def test_availability_block_creation(self):
        """Test creating an availability block"""
        block = AvailabilityBlock.objects.create(
            listing=self.listing,
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=3),
            is_blocked=True,
            block_reason='Maintenance'
        )
        
        self.assertEqual(block.listing, self.listing)
        self.assertTrue(block.is_blocked)
        self.assertEqual(block.block_reason, 'Maintenance')

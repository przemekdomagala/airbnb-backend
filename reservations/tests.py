# reservations/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Property, Reservation

User = get_user_model()

class ReservationAPITest(APITestCase):
    def setUp(self):
        # przygotuj użytkownika i nieruchomość
        self.user = User.objects.create_user(username='test', password='pass')
        self.prop = Property.objects.create(title='Mieszkanie', address='Warszawa', price=100.00)
        self.client.force_authenticate(self.user)

    def test_create_reservation(self):
        url = reverse('reservation-list-create')
        data = {
            'user': self.user.pk,
            'property': self.prop.pk,
            'start_date': '2025-06-01',
            'end_date': '2025-06-05'
        }
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(Reservation.objects.first().status, 'pending')

    def test_cancel_reservation(self):
        # najpierw utwórz rezerwację
        res = Reservation.objects.create(
            user=self.user, property=self.prop,
            start_date='2025-06-10', end_date='2025-06-12'
        )
        url = reverse('reservation-cancel', kwargs={'pk': res.pk})
        resp = self.client.patch(url, {}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        res.refresh_from_db()
        self.assertEqual(res.status, 'cancelled')
        
    def test_get_reservation_history(self):
        # Create multiple reservations for the user
        res1 = Reservation.objects.create(
            user=self.user, property=self.prop,
            start_date='2025-06-10', end_date='2025-06-12',
            status='confirmed'
        )
        res2 = Reservation.objects.create(
            user=self.user, property=self.prop,
            start_date='2025-07-10', end_date='2025-07-12',
            status='pending'
        )
        
        # Test user history
        url = reverse('reservation-history')
        resp = self.client.get(f"{url}?user_id={self.user.id}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # Check that both reservations are returned
        self.assertEqual(len(resp.data), 2)
        
        # Test property history
        resp = self.client.get(f"{url}?property_id={self.prop.id}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # Check that both reservations are returned
        self.assertEqual(len(resp.data), 2)
        
        # Test invalid request (no parameters)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

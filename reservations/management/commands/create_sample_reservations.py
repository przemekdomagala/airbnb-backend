from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date, timedelta
import random

from listings.models import Listing
from reservations.models import Reservation, ReservationPayment, AvailabilityBlock

User = get_user_model()


class Command(BaseCommand):
    help = 'Create sample reservation data for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of reservations to create',
        )

    def handle(self, *args, **options):
        count = options['count']
        
        # Get or create sample users
        guest_user, created = User.objects.get_or_create(
            username='guest_user',
            defaults={
                'email': 'guest@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'role': 'guest'
            }
        )
        if created:
            guest_user.set_password('password123')
            guest_user.save()
            self.stdout.write(f'Created guest user: {guest_user.username}')

        # Get available listings
        listings = list(Listing.objects.all())
        if not listings:
            self.stdout.write(
                self.style.ERROR('No listings found. Please create some listings first.')
            )
            return

        # Sample guest data
        sample_guests = [
            {'first_name': 'John', 'last_name': 'Doe', 'email': 'john.doe@example.com', 'phone': '+1234567890'},
            {'first_name': 'Jane', 'last_name': 'Smith', 'email': 'jane.smith@example.com', 'phone': '+1234567891'},
            {'first_name': 'Alice', 'last_name': 'Johnson', 'email': 'alice.johnson@example.com', 'phone': '+1234567892'},
            {'first_name': 'Bob', 'last_name': 'Wilson', 'email': 'bob.wilson@example.com', 'phone': '+1234567893'},
            {'first_name': 'Emma', 'last_name': 'Brown', 'email': 'emma.brown@example.com', 'phone': '+1234567894'},
        ]

        statuses = ['pending', 'confirmed', 'cancelled', 'completed']
        payment_statuses = ['pending', 'paid', 'refunded']
        payment_methods = ['card', 'paypal']

        reservations_created = 0
        
        for i in range(count):
            listing = random.choice(listings)
            guest_data = random.choice(sample_guests)
            
            # Generate random dates
            start_offset = random.randint(1, 30)  # 1 to 30 days from now
            duration = random.randint(1, 7)  # 1 to 7 nights
            
            check_in = date.today() + timedelta(days=start_offset)
            check_out = check_in + timedelta(days=duration)
            
            # Check if dates are available
            overlapping = AvailabilityBlock.objects.filter(
                listing=listing,
                start_date__lt=check_out,
                end_date__gt=check_in
            ).exists()
            
            if overlapping:
                continue  # Skip this iteration if dates overlap
            
            # Calculate pricing
            price_per_night = listing.price_per_night
            subtotal = price_per_night * duration
            taxes_and_fees = subtotal * Decimal('0.15')  # 15% taxes
            total_amount = subtotal + taxes_and_fees
            
            # Create reservation
            status = random.choice(statuses)
            payment_status = random.choice(payment_statuses)
            
            # Adjust payment status based on reservation status
            if status == 'confirmed':
                payment_status = 'paid'
            elif status == 'cancelled':
                payment_status = random.choice(['refunded', 'paid'])
            elif status == 'pending':
                payment_status = 'pending'
            
            reservation = Reservation.objects.create(
                user=guest_user,
                listing=listing,
                check_in=check_in,
                check_out=check_out,
                guests_adults=random.randint(1, 4),
                guests_children=random.randint(0, 2),
                total_nights=duration,
                guest_first_name=guest_data['first_name'],
                guest_last_name=guest_data['last_name'],
                guest_email=guest_data['email'],
                guest_phone=guest_data['phone'],
                special_requests=random.choice([
                    '', 'Late check-in', 'Early check-out', 'Extra towels',
                    'Quiet room', 'High floor', 'Ground floor access'
                ]),
                price_per_night=price_per_night,
                subtotal=subtotal,
                taxes_and_fees=taxes_and_fees,
                total_amount=total_amount,
                status=status,
                payment_status=payment_status,
                payment_method=random.choice(payment_methods)
            )
            
            # Create availability block
            AvailabilityBlock.objects.create(
                listing=listing,
                start_date=check_in,
                end_date=check_out,
                reservation=reservation
            )
            
            # Create payment record if paid
            if payment_status == 'paid':
                ReservationPayment.objects.create(
                    reservation=reservation,
                    payment_provider='stripe',
                    card_last_four=str(random.randint(1000, 9999)),
                    card_brand=random.choice(['Visa', 'Mastercard', 'American Express']),
                    amount_paid=total_amount,
                    paid_at=reservation.created_at
                )
            
            reservations_created += 1
            self.stdout.write(f'Created reservation: {reservation.confirmation_number}')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {reservations_created} reservations')
        )

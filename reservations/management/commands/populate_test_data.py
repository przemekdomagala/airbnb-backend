import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from reservations.models import (
    Property, CancellationPolicy, SpecialOffer, Reservation,
    ReservationInvoice, ReservationNotification
)
from reviews.models import Review, ReviewResponse

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with sample data for testing the API endpoints'

    def handle(self, *args, **options):
        self.stdout.write('Creating test data...')
        
        # Create users if they don't exist
        users = self.create_users()
        
        # Create properties
        properties = self.create_properties()
        
        # Create cancellation policies
        policies = self.create_cancellation_policies()
        
        # Create special offers
        offers = self.create_special_offers(properties)
        
        # Create reservations
        reservations = self.create_reservations(users, properties)
        
        # Create reviews
        reviews = self.create_reviews(reservations)
        
        self.stdout.write(self.style.SUCCESS('Successfully created test data!'))
        self.stdout.write(f'Created {len(users)} users')
        self.stdout.write(f'Created {len(properties)} properties')
        self.stdout.write(f'Created {len(policies)} cancellation policies')
        self.stdout.write(f'Created {len(offers)} special offers')
        self.stdout.write(f'Created {len(reservations)} reservations')
        self.stdout.write(f'Created {len(reviews)} reviews')
        self.stdout.write("\nYou can now test your API endpoints in the browser:")
        self.stdout.write("- http://127.0.0.1:8000/api/reservations/properties/")
        self.stdout.write("- http://127.0.0.1:8000/api/reservations/offers/")
        self.stdout.write("- http://127.0.0.1:8000/api/reservations/")
        self.stdout.write("- http://127.0.0.1:8000/api/reviews/")
    
    def create_users(self):
        users = []
        # Admin user
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@example.com', 'password123')
            users.append(admin)
        
        # Regular users
        test_users = [
            {'username': 'john', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'jane', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'username': 'robert', 'email': 'robert@example.com', 'first_name': 'Robert', 'last_name': 'Johnson'}
        ]
        
        for user_data in test_users:
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password='password123',
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name']
                )
                users.append(user)
        
        return users
    
    def create_properties(self):
        property_data = [
            {
                'title': 'Beachfront Villa',
                'address': '123 Ocean Drive, Miami, FL',
                'price': 350.00
            },
            {
                'title': 'Mountain Cabin',
                'address': '456 Pine Road, Aspen, CO',
                'price': 220.00
            },
            {
                'title': 'Downtown Loft',
                'address': '789 Main Street, New York, NY',
                'price': 180.00
            },
            {
                'title': 'Lakeside Cottage',
                'address': '101 Lake View, Lake Tahoe, CA',
                'price': 200.00
            },
            {
                'title': 'Country House',
                'address': '202 Farm Lane, Nashville, TN',
                'price': 150.00
            }
        ]
        
        properties = []
        for data in property_data:
            prop, created = Property.objects.get_or_create(
                title=data['title'],
                defaults={
                    'address': data['address'],
                    'price': data['price']
                }
            )
            properties.append(prop)
        
        return properties
    
    def create_cancellation_policies(self):
        policy_data = [
            {
                'name': 'Flexible',
                'description': 'Full refund 1 day prior to arrival',
                'refundable_until': timedelta(days=1)
            },
            {
                'name': 'Moderate',
                'description': 'Full refund 5 days prior to arrival',
                'refundable_until': timedelta(days=5)
            },
            {
                'name': 'Strict',
                'description': 'Full refund 14 days prior to arrival',
                'refundable_until': timedelta(days=14)
            }
        ]
        
        policies = []
        for data in policy_data:
            policy, created = CancellationPolicy.objects.get_or_create(
                name=data['name'],
                defaults={
                    'description': data['description'],
                    'refundable_until': data['refundable_until']
                }
            )
            policies.append(policy)
        
        return policies
    
    def create_special_offers(self, properties):
        # Clear existing offers
        SpecialOffer.objects.all().delete()
        
        offers = []
        start_date = timezone.now().date()
        
        for i, prop in enumerate(properties):
            offer = SpecialOffer.objects.create(
                property=prop,
                name=f'Special Offer {i+1}',
                discount_percent=random.randint(5, 25),
                start_date=start_date,
                end_date=start_date + timedelta(days=30)
            )
            offers.append(offer)
        
        return offers
    
    def create_reservations(self, users, properties):
        # Clear existing reservations
        Reservation.objects.all().delete()
        ReservationInvoice.objects.all().delete()
        
        reservations = []
        statuses = ['pending', 'confirmed', 'cancelled', 'completed']
        
        today = timezone.now().date()
        
        # Create some past reservations
        for i in range(10):
            start_date = today - timedelta(days=random.randint(60, 90))
            end_date = start_date + timedelta(days=random.randint(3, 10))
            user = random.choice(users)
            property_obj = random.choice(properties)
            
            reservation = Reservation.objects.create(
                user=user,
                property=property_obj,
                start_date=start_date,
                end_date=end_date,
                status='completed'
            )
            
            # Create invoice for this reservation
            ReservationInvoice.objects.create(
                reservation=reservation,
                amount=property_obj.price * (end_date - start_date).days
            )
            
            reservations.append(reservation)
        
        # Create some current and future reservations
        for i in range(15):
            # 50% chance of current reservation, 50% chance of future
            if random.random() < 0.5:
                start_date = today - timedelta(days=random.randint(1, 5))
                end_date = today + timedelta(days=random.randint(1, 5))
                status = 'confirmed'
            else:
                start_date = today + timedelta(days=random.randint(5, 60))
                end_date = start_date + timedelta(days=random.randint(3, 10))
                status = random.choice(statuses)
            
            user = random.choice(users)
            property_obj = random.choice(properties)
            
            reservation = Reservation.objects.create(
                user=user,
                property=property_obj,
                start_date=start_date,
                end_date=end_date,
                status=status
            )
            
            # Create invoice for this reservation
            ReservationInvoice.objects.create(
                reservation=reservation,
                amount=property_obj.price * (end_date - start_date).days
            )
            
            # Create notification for some reservations
            if random.random() < 0.7:
                ReservationNotification.objects.create(
                    reservation=reservation,
                    message=f"Your reservation for {property_obj.title} has been {status}."
                )
            
            reservations.append(reservation)
        
        return reservations
    
    def create_reviews(self, reservations):
        # Clear existing reviews
        Review.objects.all().delete()
        ReviewResponse.objects.all().delete()
        
        reviews = []
        completed_reservations = [r for r in reservations if r.status == 'completed']
        
        for reservation in completed_reservations:
            if random.random() < 0.8:  # 80% of completed reservations have reviews
                review = Review.objects.create(
                    reservation=reservation,
                    user=reservation.user,
                    rating=random.randint(3, 5),  # Biased towards positive reviews
                    text=f"Great stay at {reservation.property.title}. Would recommend!"
                )
                
                # 50% of reviews get responses
                if random.random() < 0.5:
                    ReviewResponse.objects.create(
                        review=review,
                        user=User.objects.get(username='admin'),  # Admin responds as property owner
                        text="Thank you for your review! We hope to see you again soon."
                    )
                
                reviews.append(review)
        
        return reviews
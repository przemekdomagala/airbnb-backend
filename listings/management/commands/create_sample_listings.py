from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Listing
from decimal import Decimal

User = get_user_model()


class Command(BaseCommand):
    help = 'Create sample listings for testing'

    def handle(self, *args, **options):
        # Create a default user if none exists
        if not User.objects.exists():
            user = User.objects.create_user(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            self.stdout.write(f'Created user: {user.username}')
        else:
            user = User.objects.first()

        # Sample listings data
        listings_data = [
            {
                'title': 'Grand Plaza Hotel',
                'description': 'Luxury hotel in the heart of the city with stunning views and world-class amenities.',
                'price_per_night': Decimal('299.99'),
                'location': 'Central Park, New York',
                'latitude': Decimal('40.7829'),
                'longitude': Decimal('-73.9654'),
                'image_url': 'https://example.com/grand-plaza.jpg'
            },
            {
                'title': 'Luxury Suite Downtown',
                'description': 'Elegant suite with premium furnishings and exceptional service.',
                'price_per_night': Decimal('449.99'),
                'location': 'Downtown Manhattan, New York',
                'latitude': Decimal('40.7589'),
                'longitude': Decimal('-73.9851'),
                'image_url': 'https://example.com/luxury-suite.jpg'
            },
            {
                'title': 'Cozy Apartment Brooklyn',
                'description': 'Charming apartment in a quiet neighborhood with modern amenities.',
                'price_per_night': Decimal('129.99'),
                'location': 'Brooklyn, New York',
                'latitude': Decimal('40.6782'),
                'longitude': Decimal('-73.9442'),
                'image_url': 'https://example.com/cozy-apartment.jpg'
            },
            {
                'title': 'Modern Loft SoHo',
                'description': 'Stylish loft in the trendy SoHo district with artistic flair.',
                'price_per_night': Decimal('389.99'),
                'location': 'SoHo, New York',
                'latitude': Decimal('40.7233'),
                'longitude': Decimal('-74.0030'),
                'image_url': 'https://example.com/modern-loft.jpg'
            },
            {
                'title': 'Seaside Villa Hamptons',
                'description': 'Beautiful oceanfront villa with private beach access.',
                'price_per_night': Decimal('799.99'),
                'location': 'The Hamptons, New York',
                'latitude': Decimal('40.9176'),
                'longitude': Decimal('-72.3951'),
                'image_url': 'https://example.com/seaside-villa.jpg'
            }
        ]

        # Create listings
        for idx, listing_data in enumerate(listings_data, 1):
            listing, created = Listing.objects.get_or_create(
                id=idx,
                defaults={
                    'owner': user,
                    **listing_data
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created listing #{listing.id}: {listing.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Listing #{listing.id} already exists: {listing.title}')
                )

        self.stdout.write(self.style.SUCCESS('Sample listings creation completed!'))

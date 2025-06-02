import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from listings.models import Listing

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with sample listings data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample listings...')
        
        # Create test users if they don't exist
        users = self.create_users()
        
        # Create listings
        listings = self.create_listings(users)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(listings)} listings!'))
    
    def create_users(self):
        users = []
        user_data = [
            {'username': 'host1', 'email': 'host1@example.com', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'host2', 'email': 'host2@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'username': 'host3', 'email': 'host3@example.com', 'first_name': 'Alex', 'last_name': 'Johnson'}
        ]
        
        for data in user_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name']
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Created user: {user.username}')
            users.append(user)
        
        return users
    
    def create_listings(self, users):
        # Sample data for listings
        locations_with_coords = [
            {
                'name': 'New York, NY', 
                'lat': 40.712776, 
                'lng': -74.005974,
                'images': [
                    'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?q=80&w=1000&auto=format&fit=crop',
                    'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?q=80&w=1000&auto=format&fit=crop'
                ]
            },
            {
                'name': 'Los Angeles, CA', 
                'lat': 34.052235, 
                'lng': -118.243683,
                'images': [
                    'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?q=80&w=1000&auto=format&fit=crop',
                    'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?q=80&w=1000&auto=format&fit=crop'
                ]
            },
            {
                'name': 'Chicago, IL', 
                'lat': 41.878113, 
                'lng': -87.629799,
                'images': [
                    'https://images.unsplash.com/photo-1566073771259-6a8506099945?q=80&w=1000&auto=format&fit=crop',
                    'https://images.unsplash.com/photo-1566073771259-6a8506099945?q=80&w=1000&auto=format&fit=crop'
                ]
            },
            {
                'name': 'Miami, FL', 
                'lat': 25.761681, 
                'lng': -80.191788,
                'images': [
                    'https://images.unsplash.com/photo-1582719508461-905c673771fd?q=80&w=1000&auto=format&fit=crop',
                    'https://images.unsplash.com/photo-1582719508461-905c673771fd?q=80&w=1000&auto=format&fit=crop'
                ]
            },
            {
                'name': 'Seattle, WA', 
                'lat': 47.606209, 
                'lng': -122.332069,
                'images': [
                    'https://images.unsplash.com/photo-1582719508461-905c673771fd?q=80&w=1000&auto=format&fit=crop',
                    'https://images.unsplash.com/photo-1582719508461-905c673771fd?q=80&w=1000&auto=format&fit=crop'
                ]
            },
        ]
        
        listing_titles = [
            'Cozy apartment in the heart of the city',
            'Modern loft with stunning views',
            'Charming studio near downtown',
            'Luxury penthouse with rooftop terrace',
            'Spacious family home near the beach',
            'Urban retreat with city skyline views',
            'Stylish condo with pool access',
            'Historic townhouse in quaint neighborhood',
            'Waterfront cottage with private dock',
            'Contemporary villa with garden'
        ]
        
        descriptions = [
            'This beautiful space offers all the comforts of home with a prime location for exploring the city.',
            'Enjoy your stay in this carefully designed space with modern amenities and convenient access to local attractions.',
            'Perfect for travelers seeking comfort and convenience, this property provides an ideal base for your visit.',
            'Experience luxury living in this exceptional property featuring high-end finishes and breathtaking views.',
            'Relax in style in this thoughtfully appointed accommodation with all the essentials for a memorable stay.'
        ]
        
        listings = []
        for i in range(15):  # Create 15 listings
            loc = random.choice(locations_with_coords)
            title = random.choice(listing_titles)
            description = random.choice(descriptions) + ' ' + random.choice(descriptions)
            price = round(random.uniform(50, 500), 2)
            owner = random.choice(users)
            image = random.choice(loc['images'])
            
            # Create variation in coordinates to spread listings around
            lat_variation = random.uniform(-0.02, 0.02)
            lng_variation = random.uniform(-0.02, 0.02)
            
            listing = Listing.objects.create(
                title=title,
                description=description,
                price_per_night=price,
                location=loc['name'],
                latitude=loc['lat'] + lat_variation,
                longitude=loc['lng'] + lng_variation,
                image_url=image,
                owner=owner
            )
            listings.append(listing)
            self.stdout.write(f'Created listing: {listing.title} in {listing.location}')
        
        return listings
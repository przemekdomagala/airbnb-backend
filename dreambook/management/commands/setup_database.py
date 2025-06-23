import random
from datetime import datetime, timedelta, date
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction

# Import all your models
from accounts.models import CustomUser
from listings.models import (
    Listing, Advertisement, AdvertisementCategory, PropertyImages,
    RentalAdvertisement, HotelAdvertisement, HotelRoom, PremiumAdvertisement,
    SeasonalAdvertisement, AdvertisementTag, AdvertisementPricing,
    AdvertisementStatistics, AdvertisementSchedule, AdvertisementReport
)
from reservations.models import (
    Property, CancellationPolicy, SpecialOffer, Reservation,
    ReservationInvoice, ReservationNotification
)
from reviews.models import Review, ReviewResponse
from hosts.models import Host, HostAvailability
from map.models import Location, MapMarker, POI
from user_management.models import Role, Permission, RolePermission, UserRole
from filtering_sorting.models import Property as FilterProperty

User = get_user_model()

class Command(BaseCommand):
    help = 'Complete database setup with all sample data after migration reset'

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-users',
            action='store_true',
            help='Skip creating users (if they already exist)',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Setting up complete database...'))
        
        try:
            with transaction.atomic():
                # Create users first (they're referenced by many models)
                if not options['skip_users']:
                    users = self.create_users()
                else:
                    users = list(User.objects.all())
                    self.stdout.write('Skipping user creation, using existing users')
                
                # Create all other data
                self.create_roles_and_permissions()
                hosts = self.create_hosts()
                locations = self.create_locations()
                listings = self.create_listings(users)
                properties = self.create_properties()
                policies = self.create_cancellation_policies()
                offers = self.create_special_offers(properties)
                reservations = self.create_reservations(users, properties)
                reviews = self.create_reviews(reservations)
                filter_properties = self.create_filter_properties()
                categories = self.create_advertisement_categories()
                advertisements = self.create_advertisements(users, categories)
                
                self.assign_user_roles(users)
                
                self.stdout.write(self.style.SUCCESS('✅ Database setup completed successfully!'))
                self.print_summary(users, hosts, locations, listings, properties, reservations, reviews, advertisements)
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error during setup: {str(e)}'))
            raise

    def create_users(self):
        self.stdout.write('Creating users...')
        users = []
        
        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@dreambook.com',
                password='admin123',
                phone_number='+1234567890'
            )
            users.append(admin)
            self.stdout.write(f'Created superuser: {admin.username}')
        
        # Create regular users
        user_data = [
            {
                'username': 'john_doe',
                'email': 'john@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'phone_number': '+1234567891'
            },
            {
                'username': 'jane_smith',
                'email': 'jane@example.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'phone_number': '+1234567892'
            },
            {
                'username': 'robert_johnson',
                'email': 'robert@example.com',
                'first_name': 'Robert',
                'last_name': 'Johnson',
                'phone_number': '+1234567893'
            },
            {
                'username': 'host1',
                'email': 'host1@example.com',
                'first_name': 'Host',
                'last_name': 'One',
                'phone_number': '+1234567894'
            },
            {
                'username': 'host2',
                'email': 'host2@example.com',
                'first_name': 'Host',
                'last_name': 'Two',
                'phone_number': '+1234567895'
            }
        ]
        
        for data in user_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'phone_number': data['phone_number']
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Created user: {user.username}')
            users.append(user)
        
        return users

    def create_roles_and_permissions(self):
        self.stdout.write('Creating roles and permissions...')
        
        # Create roles
        roles_data = [
            {'name': 'ADMIN', 'description': 'System administrator'},
            {'name': 'HOST', 'description': 'Property host'},
            {'name': 'CLIENT', 'description': 'Regular client'},
            {'name': 'GUEST', 'description': 'Guest user'},
        ]
        
        for role_data in roles_data:
            role, created = Role.objects.get_or_create(
                name=role_data['name'],
                defaults={'description': role_data['description']}
            )
            if created:
                self.stdout.write(f'Created role: {role.name}')
        
        # Create permissions
        permissions_data = [
            {'name': 'can_create_listing', 'description': 'Can create property listings'},
            {'name': 'can_manage_reservations', 'description': 'Can manage reservations'},
            {'name': 'can_write_reviews', 'description': 'Can write reviews'},
            {'name': 'can_access_admin', 'description': 'Can access admin panel'},
        ]
        
        for perm_data in permissions_data:
            permission, created = Permission.objects.get_or_create(
                name=perm_data['name'],
                defaults={'description': perm_data['description']}
            )
            if created:
                self.stdout.write(f'Created permission: {permission.name}')

    def assign_user_roles(self, users):
        self.stdout.write('Assigning roles to users...')
        
        # Get roles
        admin_role = Role.objects.get(name='ADMIN')
        host_role = Role.objects.get(name='HOST')
        client_role = Role.objects.get(name='CLIENT')
        
        # Assign roles
        for user in users:
            if user.username == 'admin':
                UserRole.objects.get_or_create(user=user, role=admin_role)
            elif 'host' in user.username:
                UserRole.objects.get_or_create(user=user, role=host_role)
            else:
                UserRole.objects.get_or_create(user=user, role=client_role)

    def create_hosts(self):
        self.stdout.write('Creating hosts...')
        hosts = []
        
        host_data = [
            {
                'user_id': 1,
                'name': 'Jan Kowalski',
                'location': 'Warszawa, Polska',
                'rating': 4.8,
                'image': 'https://images.unsplash.com/photo-1582719508461-905c673771fd?q=80&w=1000&auto=format&fit=crop',
                'details': 'Experienced host in Warsaw city center'
            },
            {
                'user_id': 2,
                'name': 'Anna Nowak',
                'location': 'Kraków, Polska',
                'rating': 4.6,
                'image': 'https://images.unsplash.com/photo-1568084680786-a84f91d1153c?q=80&w=1000&auto=format&fit=crop',
                'details': 'Mountain lover and hiking guide'
            },
            {
                'user_id': 3,
                'name': 'Piotr Wiśniewski',
                'location': 'Gdańsk, Polska',
                'rating': 4.9,
                'image': 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?q=80&w=1000&auto=format&fit=crop',
                'details': 'Seaside property specialist'
            }
        ]
        
        for data in host_data:
            host, created = Host.objects.get_or_create(
                user_id=data['user_id'],
                defaults={
                    'name': data['name'],
                    'location': data['location'],
                    'rating': data['rating'],
                    'image': data['image'],
                    'details': data['details']
                }
            )
            if created:
                self.stdout.write(f'Created host: {host.name}')
                
                # Create availability for this host
                HostAvailability.objects.get_or_create(
                    host=host,
                    start_date=date.today(),
                    end_date=date.today() + timedelta(days=30)
                )
            hosts.append(host)
        
        return hosts

    def create_locations(self):
        self.stdout.write('Creating map locations...')
        locations = []
        
        location_data = [
            {'name': 'Central Park Hotel', 'location': 'New York', 'latitude': 40.7829, 'longitude': -73.9654},
            {'name': 'Beach Resort', 'location': 'Miami', 'latitude': 25.7617, 'longitude': -80.1918},
            {'name': 'Mountain Lodge', 'location': 'Denver', 'latitude': 39.7392, 'longitude': -104.9903},
            {'name': 'City Center Apartment', 'location': 'Chicago', 'latitude': 41.8781, 'longitude': -87.6298}
        ]
        
        for data in location_data:
            location, created = Location.objects.get_or_create(
                name=data['name'],
                defaults={
                    'location': data['location'],
                    'latitude': data['latitude'],
                    'longitude': data['longitude']
                }
            )
            if created:
                self.stdout.write(f'Created location: {location.name}')
                
                # Create markers and POIs
                MapMarker.objects.get_or_create(
                    location=location,
                    marker_type='property',
                    label=f'Marker for {location.name}'
                )
                
                POI.objects.get_or_create(
                    location=location,
                    name=f'Nearby attraction to {location.name}',
                    description='Popular local attraction'
                )
            
            locations.append(location)
        
        return locations

    def create_listings(self, users):
        self.stdout.write('Creating listings...')
        listings = []
        
        locations_with_coords = [
            {'name': 'New York, NY', 'lat': 40.7128, 'lng': -74.0060},
            {'name': 'Los Angeles, CA', 'lat': 34.0522, 'lng': -118.2437},
            {'name': 'Chicago, IL', 'lat': 41.8781, 'lng': -87.6298},
            {'name': 'Miami, FL', 'lat': 25.7617, 'lng': -80.1918},
            {'name': 'Seattle, WA', 'lat': 47.6062, 'lng': -122.3321}
        ]
        
        listing_titles = [
            'Cozy Downtown Apartment',
            'Modern Loft with City Views',
            'Spacious Family Home',
            'Luxury Penthouse Suite',
            'Charming Studio Near Beach'
        ]
        
        for i in range(10):
            loc = random.choice(locations_with_coords)
            title = random.choice(listing_titles)
            owner = random.choice(users)
            
            listing = Listing.objects.create(
                title=title,
                description=f'Beautiful {title.lower()} in {loc["name"]}',
                price_per_night=round(random.uniform(80, 400), 2),
                location=loc['name'],
                latitude=loc['lat'] + random.uniform(-0.01, 0.01),
                longitude=loc['lng'] + random.uniform(-0.01, 0.01),
                image_url='https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?q=80&w=1000&auto=format&fit=crop',
                owner=owner
            )
            listings.append(listing)
        
        self.stdout.write(f'Created {len(listings)} listings')
        return listings

    def create_properties(self):
        self.stdout.write('Creating properties...')
        properties = []
        
        property_data = [
            {'title': 'Beachfront Villa', 'address': '123 Ocean Drive, Miami, FL', 'price': 350.00},
            {'title': 'Mountain Cabin', 'address': '456 Pine Road, Aspen, CO', 'price': 220.00},
            {'title': 'Downtown Loft', 'address': '789 Main Street, New York, NY', 'price': 180.00},
            {'title': 'Lakeside Cottage', 'address': '101 Lake View, Lake Tahoe, CA', 'price': 200.00},
            {'title': 'Country House', 'address': '202 Farm Lane, Nashville, TN', 'price': 150.00}
        ]
        
        for data in property_data:
            prop, created = Property.objects.get_or_create(
                title=data['title'],
                defaults={
                    'address': data['address'],
                    'price': data['price']
                }
            )
            if created:
                self.stdout.write(f'Created property: {prop.title}')
            properties.append(prop)
        
        return properties

    def create_cancellation_policies(self):
        self.stdout.write('Creating cancellation policies...')
        policies = []
        
        policy_data = [
            {'name': 'Flexible', 'description': 'Full refund 1 day prior', 'refundable_until': timedelta(days=1)},
            {'name': 'Moderate', 'description': 'Full refund 5 days prior', 'refundable_until': timedelta(days=5)},
            {'name': 'Strict', 'description': 'Full refund 14 days prior', 'refundable_until': timedelta(days=14)}
        ]
        
        for data in policy_data:
            policy, created = CancellationPolicy.objects.get_or_create(
                name=data['name'],
                defaults={
                    'description': data['description'],
                    'refundable_until': data['refundable_until']
                }
            )
            if created:
                self.stdout.write(f'Created policy: {policy.name}')
            policies.append(policy)
        
        return policies

    def create_special_offers(self, properties):
        self.stdout.write('Creating special offers...')
        offers = []
        
        start_date = timezone.now().date()
        for i, prop in enumerate(properties[:3]):  # Create offers for first 3 properties
            offer = SpecialOffer.objects.create(
                property=prop,
                name=f'Summer Special {i+1}',
                discount_percent=random.randint(10, 30),
                start_date=start_date,
                end_date=start_date + timedelta(days=60)
            )
            offers.append(offer)
        
        self.stdout.write(f'Created {len(offers)} special offers')
        return offers

    def create_reservations(self, users, properties):
        self.stdout.write('Creating reservations...')
        reservations = []
        statuses = ['pending', 'confirmed', 'cancelled', 'completed']
        
        today = timezone.now().date()
        
        for i in range(15):
            # Mix of past, current, and future reservations
            if i < 5:  # past reservations
                start_date = today - timedelta(days=random.randint(30, 90))
                end_date = start_date + timedelta(days=random.randint(3, 7))
                status = 'completed'
            elif i < 10:  # current/near future
                start_date = today + timedelta(days=random.randint(1, 30))
                end_date = start_date + timedelta(days=random.randint(3, 7))
                status = random.choice(['pending', 'confirmed'])
            else:  # future reservations
                start_date = today + timedelta(days=random.randint(30, 90))
                end_date = start_date + timedelta(days=random.randint(3, 7))
                status = 'pending'
            
            reservation = Reservation.objects.create(
                user=random.choice(users),
                property=random.choice(properties),
                start_date=start_date,
                end_date=end_date,
                status=status
            )
            
            # Create invoice
            ReservationInvoice.objects.create(
                reservation=reservation,
                amount=reservation.property.price * (end_date - start_date).days
            )
            
            # Create notification
            if random.random() < 0.7:
                ReservationNotification.objects.create(
                    reservation=reservation,
                    message=f'Your reservation for {reservation.property.title} has been {status}.'
                )
            
            reservations.append(reservation)
        
        self.stdout.write(f'Created {len(reservations)} reservations')
        return reservations

    def create_reviews(self, reservations):
        self.stdout.write('Creating reviews...')
        reviews = []
        
        completed_reservations = [r for r in reservations if r.status == 'completed']
        
        for reservation in completed_reservations:
            if random.random() < 0.8:  # 80% of completed reservations get reviews
                review = Review.objects.create(
                    reservation=reservation,
                    user=reservation.user,
                    rating=random.randint(3, 5),
                    text=f'Great stay at {reservation.property.title}. Highly recommended!'
                )
                
                # 50% chance of getting a response
                if random.random() < 0.5:
                    admin_user = User.objects.filter(username='admin').first()
                    if admin_user:
                        ReviewResponse.objects.create(
                            review=review,
                            user=admin_user,
                            text='Thank you for your wonderful review! We hope to host you again soon.'
                        )
                
                reviews.append(review)
        
        self.stdout.write(f'Created {len(reviews)} reviews')
        return reviews

    def create_filter_properties(self):
        self.stdout.write('Creating filter properties...')
        properties = []
        
        locations = ['New York', 'Los Angeles', 'Chicago', 'Miami', 'Seattle']
        property_types = ['apartment', 'house', 'condo', 'villa', 'studio']
        amenities_options = [
            ['wifi', 'parking', 'gym'],
            ['wifi', 'pool', 'kitchen'],
            ['wifi', 'parking', 'balcony'],
            ['wifi', 'gym', 'concierge'],
            ['wifi', 'pool', 'parking', 'gym']
        ]
        
        for i in range(8):
            prop = FilterProperty.objects.create(
                title=f'Filter Property {i+1}',
                location=random.choice(locations),
                price_per_night=random.randint(50, 500),
                max_guests=random.randint(1, 8),
                available_from=timezone.now().date(),
                available_to=timezone.now().date() + timedelta(days=365),
                rating=round(random.uniform(3.0, 5.0), 1),
                amenities=random.choice(amenities_options),
                distance_to_center=round(random.uniform(0.5, 15.0), 1),
                property_type=random.choice(property_types),
                review_count=random.randint(0, 100)
            )
            properties.append(prop)
        
        self.stdout.write(f'Created {len(properties)} filter properties')
        return properties

    def create_advertisement_categories(self):
        self.stdout.write('Creating advertisement categories...')
        categories = []
        
        category_data = [
            {'name': 'Private Rentals', 'description': 'Short-term private property rentals'},
            {'name': 'Hotels', 'description': 'Hotel accommodations'},
            {'name': 'Luxury Properties', 'description': 'High-end luxury accommodations'},
            {'name': 'Budget Friendly', 'description': 'Affordable accommodation options'},
            {'name': 'Business Travel', 'description': 'Accommodations for business travelers'},
        ]
        
        for data in category_data:
            category, created = AdvertisementCategory.objects.get_or_create(
                name=data['name'],
                defaults={'description': data['description']}
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')
            categories.append(category)
        
        return categories

    def create_advertisements(self, users, categories):
        self.stdout.write('Creating advertisements (private listings and hotels)...')
        advertisements = []
        
        # Create private rental advertisements
        private_category = next((c for c in categories if c.name == 'Private Rentals'), categories[0])
        luxury_category = next((c for c in categories if c.name == 'Luxury Properties'), categories[0])
        
        private_listings_data = [
            {
                'title': 'Cozy Downtown Apartment',
                'description': 'Beautiful 2-bedroom apartment in the heart of the city with modern amenities.',
                'location': 'New York, NY',
                'latitude': 40.7589, 'longitude': -73.9851,
                'price_per_night': 180.00, 'min_stay': 2,
                'category': private_category
            },
            {
                'title': 'Beachfront Villa Paradise',
                'description': 'Stunning oceanfront villa with private beach access and infinity pool.',
                'location': 'Miami, FL',
                'latitude': 25.7617, 'longitude': -80.1918,
                'price_per_night': 450.00, 'min_stay': 3,
                'category': luxury_category
            },
            {
                'title': 'Mountain Cabin Retreat',
                'description': 'Peaceful mountain cabin perfect for a nature getaway.',
                'location': 'Aspen, CO',
                'latitude': 39.1911, 'longitude': -106.8175,
                'price_per_night': 220.00, 'min_stay': 2,
                'category': private_category
            },
            {
                'title': 'Historic Brownstone Loft',
                'description': 'Charming loft in a historic brownstone building.',
                'location': 'Boston, MA',
                'latitude': 42.3601, 'longitude': -71.0589,
                'price_per_night': 195.00, 'min_stay': 1,
                'category': private_category
            }
        ]
        
        for i, data in enumerate(private_listings_data):
            owner = users[i % len(users)]
            
            # Create advertisement
            advertisement = Advertisement.objects.create(
                title=data['title'],
                description=data['description'],
                advertisement_type='private',
                category=data['category'],
                user=owner,
                location=data['location'],
                latitude=data['latitude'],
                longitude=data['longitude'],
                status='active',
                max_guests=random.randint(2, 6),
                bedrooms=random.randint(1, 3),
                bathrooms=random.randint(1, 2)
            )
            
            # Create rental details
            RentalAdvertisement.objects.create(
                advertisement=advertisement,
                price_per_night=data['price_per_night'],
                minimum_stay=data['min_stay'],
                instant_booking=random.choice([True, False]),
                house_rules='No smoking, No pets, Quiet hours 10PM-8AM'
            )
            
            # Create pricing
            AdvertisementPricing.objects.create(
                advertisement=advertisement,
                base_price=data['price_per_night'],
                currency='USD',
                cleaning_fee=25.00,
                service_fee=15.00
            )
            
            # Create statistics
            AdvertisementStatistics.objects.create(
                advertisement=advertisement,
                view_count=random.randint(50, 500),
                click_count=random.randint(10, 100),
                favorite_count=random.randint(5, 50),
                inquiry_count=random.randint(2, 20),
                booking_count=random.randint(1, 10)
            )
            
            # Add some images
            PropertyImages.objects.create(
                advertisement=advertisement,
                image_url='https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?q=80&w=1000&auto=format&fit=crop',
                is_primary=True
            )
            
            advertisements.append(advertisement)
        
        # Create hotel advertisements
        hotel_category = next((c for c in categories if c.name == 'Hotels'), categories[0])
        business_category = next((c for c in categories if c.name == 'Business Travel'), categories[0])
        
        hotels_data = [
            {
                'title': 'Grand Metropolitan Hotel',
                'hotel_name': 'Grand Metropolitan',
                'description': 'Luxury 5-star hotel in downtown with world-class amenities.',
                'location': 'Chicago, IL',
                'latitude': 41.8781, 'longitude': -87.6298,
                'star_rating': 5,
                'category': luxury_category
            },
            {
                'title': 'Seaside Resort & Spa',
                'hotel_name': 'Seaside Resort & Spa',
                'description': 'Beautiful oceanfront resort with spa and multiple dining options.',
                'location': 'San Diego, CA',
                'latitude': 32.7157, 'longitude': -117.1611,
                'star_rating': 4,
                'category': hotel_category
            },
            {
                'title': 'Business Plaza Hotel',
                'hotel_name': 'Business Plaza',
                'description': 'Modern business hotel with conference facilities.',
                'location': 'Atlanta, GA',
                'latitude': 33.7490, 'longitude': -84.3880,
                'star_rating': 3,
                'category': business_category
            }
        ]
        
        for i, data in enumerate(hotels_data):
            owner = users[(i + len(private_listings_data)) % len(users)]
            
            # Create advertisement
            advertisement = Advertisement.objects.create(
                title=data['title'],
                description=data['description'],
                advertisement_type='hotel',
                category=data['category'],
                user=owner,
                location=data['location'],
                latitude=data['latitude'],
                longitude=data['longitude'],
                status='active',
                max_guests=4,  # Will be overridden by room capacity
                bedrooms=1,
                bathrooms=1
            )
            
            # Create hotel details
            hotel = HotelAdvertisement.objects.create(
                advertisement=advertisement,
                hotel_name=data['hotel_name'],
                star_rating=data['star_rating'],
                has_restaurant=True,
                has_spa=data['star_rating'] >= 4,
                has_gym=True,
                has_pool=data['star_rating'] >= 4,
                has_business_center=True
            )
            
            # Create hotel rooms
            room_types = [
                {'type': 'standard', 'name': 'Standard Room', 'price': 120, 'occupancy': 2, 'rooms': 50},
                {'type': 'deluxe', 'name': 'Deluxe Room', 'price': 180, 'occupancy': 2, 'rooms': 30},
                {'type': 'suite', 'name': 'Executive Suite', 'price': 350, 'occupancy': 4, 'rooms': 15}
            ]
            
            for room_data in room_types:
                HotelRoom.objects.create(
                    hotel=hotel,
                    room_type=room_data['type'],
                    room_name=room_data['name'],
                    price_per_night=room_data['price'],
                    max_occupancy=room_data['occupancy'],
                    total_rooms=room_data['rooms'],
                    room_size_sqm=random.randint(25, 60),
                    has_sea_view=random.choice([True, False]),
                    has_city_view=random.choice([True, False])
                )
            
            # Create pricing (base hotel pricing)
            AdvertisementPricing.objects.create(
                advertisement=advertisement,
                base_price=120.00,  # Starting price
                currency='USD',
                service_fee=20.00,
                tax_rate=0.12  # 12% tax
            )
            
            # Create statistics
            AdvertisementStatistics.objects.create(
                advertisement=advertisement,
                view_count=random.randint(200, 1000),
                click_count=random.randint(50, 300),
                favorite_count=random.randint(20, 100),
                inquiry_count=random.randint(10, 50),
                booking_count=random.randint(5, 30)
            )
              # Add premium features for some hotels
            if data['star_rating'] >= 4:
                PremiumAdvertisement.objects.create(
                    advertisement=advertisement,
                    is_featured=True,
                    feature_start_date=timezone.now(),
                    feature_end_date=timezone.now() + timedelta(days=30),
                    boost_priority=data['star_rating'],
                    premium_badge=True
                )
            
            # Add tags
            tags = ['luxury', 'business', 'spa', 'restaurant', 'conference'] if data['star_rating'] >= 4 else ['budget', 'business', 'convenient']
            for tag in tags[:3]:  # Add up to 3 tags
                AdvertisementTag.objects.create(
                    advertisement=advertisement,
                    tag_name=tag
                )
            
            advertisements.append(advertisement)
        
        self.stdout.write(f'Created {len(advertisements)} advertisements ({len(private_listings_data)} private, {len(hotels_data)} hotels)')
        return advertisements

    def print_summary(self, users, hosts, locations, listings, properties, reservations, reviews, advertisements):
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('📊 DATABASE SETUP SUMMARY'))
        self.stdout.write('='*50)
        self.stdout.write(f'👥 Users: {len(users)}')
        self.stdout.write(f'🏠 Hosts: {len(hosts)}')
        self.stdout.write(f'📍 Locations: {len(locations)}')
        self.stdout.write(f'🏢 Listings (Legacy): {len(listings)}')
        self.stdout.write(f'📢 Advertisements (New): {len(advertisements)}')
        self.stdout.write(f'   - Private Listings: {len([a for a in advertisements if a.advertisement_type == "private"])}')
        self.stdout.write(f'   - Hotels: {len([a for a in advertisements if a.advertisement_type == "hotel"])}')
        self.stdout.write(f'🏘️  Properties: {len(properties)}')
        self.stdout.write(f'📅 Reservations: {len(reservations)}')
        self.stdout.write(f'⭐ Reviews: {len(reviews)}')
        self.stdout.write(f'🔧 Roles: {Role.objects.count()}')
        self.stdout.write(f'🔑 Permissions: {Permission.objects.count()}')
        self.stdout.write(f'🏷️  Advertisement Categories: {AdvertisementCategory.objects.count()}')
        self.stdout.write('\n🌐 API Endpoints you can test:')
        self.stdout.write('- http://127.0.0.1:8000/api/reservations/')
        self.stdout.write('- http://127.0.0.1:8000/api/reviews/')
        self.stdout.write('- http://127.0.0.1:8000/api/listings/')
        self.stdout.write('- http://127.0.0.1:8000/api/hosts/')
        self.stdout.write('- http://127.0.0.1:8000/api/locations/')
        self.stdout.write('\n🔐 Login credentials:')
        self.stdout.write('Admin: admin / admin123')
        self.stdout.write('Users: [username] / password123')
        self.stdout.write('='*50)
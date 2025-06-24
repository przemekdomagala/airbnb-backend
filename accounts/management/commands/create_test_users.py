from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create test users for authentication testing'

    def handle(self, *args, **options):
        # Create test guest user
        if not User.objects.filter(email='guest@test.com').exists():
            guest = User.objects.create_user(
                username='testguest',
                email='guest@test.com',
                password='testpass123',
                role='guest',
                first_name='Test',
                last_name='Guest'
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created guest user: {guest.email}')
            )
        
        # Create test landlord user
        if not User.objects.filter(email='landlord@test.com').exists():
            landlord = User.objects.create_user(
                username='testlandlord',
                email='landlord@test.com',
                password='testpass123',
                role='landlord',
                first_name='Test',
                last_name='Landlord'
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created landlord user: {landlord.email}')
            )
        
        # Create test admin user
        if not User.objects.filter(email='admin@test.com').exists():
            admin = User.objects.create_superuser(
                username='testadmin',
                email='admin@test.com',
                password='testpass123',
                role='admin',
                first_name='Test',
                last_name='Admin'
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created admin user: {admin.email}')
            )

        self.stdout.write(
            self.style.SUCCESS('Test users created successfully!')
        )
        self.stdout.write('Test credentials:')
        self.stdout.write('Guest: guest@test.com / testpass123')
        self.stdout.write('Landlord: landlord@test.com / testpass123')
        self.stdout.write('Admin: admin@test.com / testpass123')

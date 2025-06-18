from django.core.management.base import BaseCommand
from hosts.models import Host, HostAvailability
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Create sample Host and HostAvailability data'

    def handle(self, *args, **kwargs):
        host1, created = Host.objects.get_or_create(
            user_id=1,
            defaults={
                'name': 'Jan Kowalski',
                'location': 'Warszawa, Polska',
                'rating': 4.8,
                'image': 'https://images.unsplash.com/photo-1582719508461-905c673771fd?q=80&w=1000&auto=format&fit=crop',
                'details': 'Warszawiak, słucha maty, pali blanty',
            }
        )

        HostAvailability.objects.get_or_create(
            host=host1,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=10)
        )

        host2, created = Host.objects.get_or_create(
            user_id=2,
            defaults={
                'name': 'Anna Nowak',
                'location': 'Kraków, Polska',
                'rating': 4.6,
                'image': 'https://images.unsplash.com/photo-1568084680786-a84f91d1153c?q=80&w=1000&auto=format&fit=crop',
                'details': 'Nosi przy sobie maczetę, lubi chodzić po górach',
            }
        )

        HostAvailability.objects.get_or_create(
            host=host2,
            start_date=date.today() + timedelta(days=5),
            end_date=date.today() + timedelta(days=15)
        )

        host3, created = Host.objects.get_or_create(
            user_id=3,
            defaults={
                'name': 'Piotr Wiśniewski',
                'location': 'Gdańsk, Polska',
                'rating': 4.9,
                'image': 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?q=80&w=1000&auto=format&fit=crop',
                'details': 'Gdańszczanin, fan piłki nożnej, lubi grać w szachy',
            }
        )

        HostAvailability.objects.get_or_create(
            host=host3,
            start_date=date.today() + timedelta(days=2),
            end_date=date.today() + timedelta(days=12)
        )

        self.stdout.write(self.style.SUCCESS('Sample hosts and availabilities created.'))

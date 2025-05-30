from django.test import TestCase
from rest_framework.test import APIClient
from .models import Host

class HostModuleTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.host = Host.objects.create(
            name="Test Host",
            location="Test City",
            rating=4.5,
            image="https://example.com/test.jpg"
        )

    def test_create_host(self):
        response = self.client.post('/api/hosts/', {
            "name": "Anna Tester",
            "location": "Kraków",
            "rating": 4.9,
            "image": "https://example.com/anna.jpg"
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "Anna Tester")

    def test_get_hosts(self):
        response = self.client.get('/api/hosts/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_host_availability_post(self):
        response = self.client.post('/api/host-availability/', {
            "host": self.host.id,
            "start_date": "2025-07-01",
            "end_date": "2025-07-10"
        }, format='json')
        self.assertEqual(response.status_code, 201)

    def test_host_booking_post(self):
        response = self.client.post('/api/host-bookings/', {
            "host": self.host.id,
            "reservation_id": 101,
            "booking_date": "2025-07-15"
        }, format='json')
        self.assertEqual(response.status_code, 201)

    def test_host_message_post(self):
        response = self.client.post('/api/host-messages/', {
            "host": self.host.id,
            "user_id": 99,
            "message_text": "Hello!"
        }, format='json')
        self.assertEqual(response.status_code, 201)

    def test_host_promotion_post(self):
        response = self.client.post('/api/host-promotions/', {
            "host": self.host.id,
            "promotion_details": "20% off!",
            "start_date": "2025-07-01",
            "end_date": "2025-07-10"
        }, format='json')
        self.assertEqual(response.status_code, 201)

    def test_host_statistics_post(self):
        response = self.client.post('/api/host-statistics/', {
            "host": self.host.id,
            "total_reservations": 5,
            "total_earnings": "1500.00"
        }, format='json')
        self.assertEqual(response.status_code, 201)

    def test_host_earnings_post(self):
        response = self.client.post('/api/host-earnings/', {
            "host": self.host.id,
            "earnings_amount": "850.00",
            "earnings_date": "2025-07-20"
        }, format='json')
        self.assertEqual(response.status_code, 201)

    def test_host_policy_post(self):
        response = self.client.post('/api/host-reservation-policy/', {
            "host": self.host.id,
            "cancellation_policy": "Free until 24h before"
        }, format='json')
        self.assertEqual(response.status_code, 201)

    def test_host_notification_post(self):
        response = self.client.post('/api/host-notifications/', {
            "host": self.host.id,
            "notification_type": "New reservation"
        }, format='json')
        self.assertEqual(response.status_code, 201)

    def test_host_support_post(self):
        response = self.client.post('/api/host-support/', {
            "host": self.host.id,
            "issue_description": "I can't edit listing",
            "status": "new"
        }, format='json')
        self.assertEqual(response.status_code, 201)

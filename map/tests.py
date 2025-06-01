from django.test import TestCase
from rest_framework.test import APIClient
from .models import Location

class MapModuleTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.location = Location.objects.create(
            name="Test Hotel",
            location="Test City",
            latitude=50.0,
            longitude=19.0
        )

    def test_create_location(self):
        response = self.client.post('/api/locations/', {
            "name": "Willa Tatry",
            "location": "Zakopane",
            "latitude": 49.29,
            "longitude": 19.95
        }, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_map_marker(self):
        response = self.client.post('/api/map-markers/', {
            "location": self.location.id,
            "marker_type": "property",
            "label": "Apartament #1"
        }, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_poi(self):
        response = self.client.post('/api/pois/', {
            "name": "Park Miejski",
            "description": "Duży park z fontanną",
            "location": self.location.id
        }, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_annotation(self):
        response = self.client.post('/api/map-annotations/', {
            "location": self.location.id,
            "text": "Świetna okolica, polecam!"
        }, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_bookmark(self):
        response = self.client.post('/api/map-bookmarks/', {
            "user_id": 123,
            "location": self.location.id
        }, format='json')
        self.assertEqual(response.status_code, 201)
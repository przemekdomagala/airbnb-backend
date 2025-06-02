# reviews/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from reservations.models import Property, Reservation
from .models import Review, ReviewResponse

User = get_user_model()

class ReviewAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='anna', password='secret')
        self.prop = Property.objects.create(title='Dom', address='Kraków', price=150.00)
        self.res = Reservation.objects.create(
            user=self.user, property=self.prop,
            start_date='2025-07-01', end_date='2025-07-03'
        )
        self.client.force_authenticate(self.user)

    def test_add_review(self):
        url = reverse('review-list-create')
        data = {
            'reservation': self.res.pk,
            'user': self.user.pk,
            'rating': 5,
            'text': 'Super pobyt!'
        }
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.first().rating, 5)

    def test_respond_to_review(self):
        review = Review.objects.create(
            reservation=self.res, user=self.user,
            rating=4, text='OK pobyt'
        )
        url = reverse('review-respond', kwargs={'pk': review.pk})
        data = {
            'review': review.pk,
            'user': self.user.pk,
            'text': 'Dziękuję za recenzję!'
        }
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ReviewResponse.objects.count(), 1)
        self.assertEqual(review.responses.count(), 1)

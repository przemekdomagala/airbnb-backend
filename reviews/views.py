# views.py
from rest_framework import generics
from .models import Review, ReviewResponse
from .serializers import ReviewSerializer, ReviewResponseSerializer

class ReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewResponseCreateAPIView(generics.CreateAPIView):
    queryset = ReviewResponse.objects.all()
    serializer_class = ReviewResponseSerializer

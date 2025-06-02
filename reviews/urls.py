from django.urls import path
from .views import ReviewListCreateAPIView, ReviewDetailAPIView, ReviewResponseCreateAPIView

urlpatterns = [
    path('', ReviewListCreateAPIView.as_view(), name='review-list-create'),
    path('<int:pk>/', ReviewDetailAPIView.as_view(), name='review-detail'),
    path('<int:pk>/respond/', ReviewResponseCreateAPIView.as_view(), name='review-respond'),
]

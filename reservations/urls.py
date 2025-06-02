from django.urls import path
from .views import (
    PropertyListCreateAPIView, PropertyDetailAPIView,
    SpecialOfferListCreateAPIView, SpecialOfferDetailAPIView,
    ReservationListCreateAPIView, ReservationDetailAPIView, CancelReservationAPIView,
    ReservationConfirmationAPIView, ReservationHistoryAPIView,
)
from .views import CheckAvailabilityAPIView

urlpatterns = [
    path('properties/', PropertyListCreateAPIView.as_view(), name='property-list-create'),
    path('properties/<int:pk>/', PropertyDetailAPIView.as_view(), name='property-detail'),

    path('offers/', SpecialOfferListCreateAPIView.as_view(), name='offer-list-create'),
    path('offers/<int:pk>/', SpecialOfferDetailAPIView.as_view(), name='offer-detail'),

    path('', ReservationListCreateAPIView.as_view(), name='reservation-list-create'),
    path('<int:pk>/', ReservationDetailAPIView.as_view(), name='reservation-detail'),
    path('<int:pk>/cancel/', CancelReservationAPIView.as_view(), name='reservation-cancel'),
    path('<int:pk>/confirm/', ReservationConfirmationAPIView.as_view(), name='reservation-confirm'),
    path('history/', ReservationHistoryAPIView.as_view(), name='reservation-history'),
    path('availability/', CheckAvailabilityAPIView.as_view(), name='check-availability'),
]

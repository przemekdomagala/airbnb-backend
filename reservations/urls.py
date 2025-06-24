from django.urls import path
from .views import (
    ReservationListCreateView, ReservationDetailView, ReservationByConfirmationView,
    AvailabilityCheckView, ReservationCancelView, ReservationConfirmView,
    user_reservation_history, landlord_reservations, AvailabilityBlockListCreateView,
    BookingStepOneView, BookingStepTwoView, BookingStepThreeView
)

app_name = 'reservations'

urlpatterns = [
    # Main reservation endpoints
    path('', ReservationListCreateView.as_view(), name='reservation-list-create'),
    path('<uuid:id>/', ReservationDetailView.as_view(), name='reservation-detail'),
    path('confirmation/<str:confirmation_number>/', ReservationByConfirmationView.as_view(), name='reservation-by-confirmation'),
    
    # Reservation actions
    path('<uuid:reservation_id>/cancel/', ReservationCancelView.as_view(), name='reservation-cancel'),
    path('<uuid:reservation_id>/confirm/', ReservationConfirmView.as_view(), name='reservation-confirm'),
    
    # History and management
    path('history/', user_reservation_history, name='user-reservation-history'),
    path('landlord/', landlord_reservations, name='landlord-reservations'),
    
    # Availability
    path('availability/check/', AvailabilityCheckView.as_view(), name='availability-check'),
    path('availability/blocks/', AvailabilityBlockListCreateView.as_view(), name='availability-blocks'),
    
    # 3-step booking process
    path('booking/step-1/', BookingStepOneView.as_view(), name='booking-step-1'),
    path('booking/step-2/', BookingStepTwoView.as_view(), name='booking-step-2'),
    path('booking/step-3/', BookingStepThreeView.as_view(), name='booking-step-3'),
]

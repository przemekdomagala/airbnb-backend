from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import AvailabilityChecker, ReservationConfirmationService, ReservationHistoryService

from .models import (
    Property, CancellationPolicy, SpecialOffer, GroupReservation, Reservation,
    ReservationDiscount, ReservationInvoice, ReservationPayment, ReservationNotification,
    ReservationReminder, ReservationExtension, ReservationModification, ReservationSupportTicket,
    ReservationOccupancy, RevenueReport, UserActivity, UserNotificationPreferences
)
from .serializers import (
    PropertySerializer, CancellationPolicySerializer, SpecialOfferSerializer, GroupReservationSerializer,
    ReservationSerializer, ReservationDiscountSerializer, ReservationInvoiceSerializer,
    ReservationPaymentSerializer, ReservationNotificationSerializer, ReservationReminderSerializer,
    ReservationExtensionSerializer, ReservationModificationSerializer, ReservationSupportTicketSerializer,
    ReservationOccupancySerializer, RevenueReportSerializer, UserActivitySerializer,
    UserNotificationPreferencesSerializer
)

class CheckAvailabilityAPIView(APIView):
    def get(self, request, *args, **kwargs):
        property_id = request.query_params.get('property_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not property_id or not start_date or not end_date:
            return Response({'error': 'Missing required parameters'}, status=status.HTTP_400_BAD_REQUEST)

        is_available = AvailabilityChecker.is_available(property_id, start_date, end_date)
        return Response({'is_available': is_available}, status=status.HTTP_200_OK)

# CRUD dla Property
class PropertyListCreateAPIView(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

class PropertyDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

# CRUD dla SpecialOffer
class SpecialOfferListCreateAPIView(generics.ListCreateAPIView):
    queryset = SpecialOffer.objects.all()
    serializer_class = SpecialOfferSerializer

class SpecialOfferDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SpecialOffer.objects.all()
    serializer_class = SpecialOfferSerializer

# CRUD dla Reservation
class ReservationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

class ReservationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

class CancelReservationAPIView(generics.UpdateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_update(self, serializer):
        serializer.save(status='cancelled')

class ReservationConfirmationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        reservation_id = request.data.get('reservation_id')
        user_id = request.data.get('user_id')

        if not reservation_id or not user_id:
            return Response({'error': 'Missing required parameters'}, status=status.HTTP_400_BAD_REQUEST)

        is_confirmed = ReservationConfirmationService.confirm(reservation_id, user_id)
        return Response({'is_confirmed': is_confirmed}, status=status.HTTP_200_OK)

class ReservationHistoryAPIView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        property_id = request.query_params.get('property_id')
        
        if user_id:
            reservations = ReservationHistoryService.get_user_reservation_history(user_id)
        elif property_id:
            reservations = ReservationHistoryService.get_property_reservation_history(property_id)
        else:
            return Response(
                {"error": "Please provide either user_id or property_id"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Inne endpointy analogicznie... (rozszerz, remind, modify, support)



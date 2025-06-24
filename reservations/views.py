from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .models import Reservation, AvailabilityBlock
from .serializers import (
    ReservationListSerializer, ReservationDetailSerializer, 
    ReservationCreateSerializer, AvailabilityCheckSerializer,
    AvailabilityBlockSerializer, ReservationPaymentSerializer
)


@method_decorator(csrf_exempt, name='dispatch')
class ReservationListCreateView(generics.ListCreateAPIView):
    """
    List all reservations for the current user or create a new reservation
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReservationCreateSerializer
        return ReservationListSerializer
    
    def get_queryset(self):
        user = self.request.user
        # Return user's reservations, with optional filtering
        queryset = Reservation.objects.filter(user=user)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)        # Filter by payment status
        payment_status = self.request.query_params.get('payment_status')
        if payment_status:
            queryset = queryset.filter(payment_status=payment_status)
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        reservation = serializer.save()
        # Return the created reservation using the detail serializer
        self.created_reservation = reservation
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Use detail serializer for response
        response_serializer = ReservationDetailSerializer(
            self.created_reservation, 
            context={'request': request}
        )
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@method_decorator(csrf_exempt, name='dispatch')
class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a reservation
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReservationDetailSerializer
    lookup_field = 'id'
    
    def get_queryset(self):
        # Users can only access their own reservations
        return Reservation.objects.filter(user=self.request.user)


@method_decorator(csrf_exempt, name='dispatch')
class ReservationByConfirmationView(generics.RetrieveAPIView):
    """
    Retrieve a reservation by confirmation number
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReservationDetailSerializer
    lookup_field = 'confirmation_number'
    
    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)


class AvailabilityCheckView(APIView):
    """
    Check if a listing is available for given dates
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = AvailabilityCheckSerializer(data=request.data)
        if serializer.is_valid():
            listing_id = serializer.validated_data['listing_id']
            check_in = serializer.validated_data['check_in']
            check_out = serializer.validated_data['check_out']
            
            # Check for overlapping reservations
            overlapping_reservations = Reservation.objects.filter(
                listing_id=listing_id,
                check_in__lt=check_out,
                check_out__gt=check_in,
                status__in=['confirmed', 'pending']
            )
            
            # Check for overlapping blocks
            overlapping_blocks = AvailabilityBlock.objects.filter(
                listing_id=listing_id,
                start_date__lt=check_out,
                end_date__gt=check_in,
                is_blocked=True
            )
            
            is_available = not (overlapping_reservations.exists() or overlapping_blocks.exists())
            
            return Response({
                'available': is_available,
                'listing_id': listing_id,
                'check_in': check_in,
                'check_out': check_out,
                'conflicts': overlapping_reservations.count() + overlapping_blocks.count() if not is_available else 0
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class ReservationCancelView(APIView):
    """
    Cancel a reservation
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, reservation_id):
        try:
            reservation = get_object_or_404(
                Reservation, 
                id=reservation_id, 
                user=request.user
            )
            
            # Check if reservation can be cancelled
            if reservation.status in ['cancelled', 'completed']:
                return Response(
                    {'error': f'Cannot cancel reservation with status: {reservation.status}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Update reservation status
            old_status = reservation.status
            reservation.status = 'cancelled'
            reservation.save()
            
            # Create status history record
            from .models import ReservationStatusHistory
            ReservationStatusHistory.objects.create(
                reservation=reservation,
                old_status=old_status,
                new_status='cancelled',
                changed_by=request.user,
                reason='Cancelled by user'
            )
            
            # Remove availability block
            AvailabilityBlock.objects.filter(reservation=reservation).delete()
            
            return Response({
                'message': 'Reservation cancelled successfully',
                'reservation_id': str(reservation.id),
                'confirmation_number': reservation.confirmation_number
            })
            
        except Reservation.DoesNotExist:
            return Response(
                {'error': 'Reservation not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


@method_decorator(csrf_exempt, name='dispatch')
class ReservationConfirmView(APIView):
    """
    Confirm a reservation (process payment)
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, reservation_id):
        try:
            reservation = get_object_or_404(
                Reservation, 
                id=reservation_id, 
                user=request.user
            )
            
            # Check if reservation can be confirmed
            if reservation.status != 'pending':
                return Response(
                    {'error': f'Cannot confirm reservation with status: {reservation.status}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Simulate payment processing
            payment_data = request.data.get('payment', {})
            card_data = payment_data.get('card', {})
            
            # Create payment record
            from .models import ReservationPayment
            payment = ReservationPayment.objects.create(
                reservation=reservation,
                payment_provider='stripe',  # Default to Stripe
                card_last_four=card_data.get('last_four', '1234'),
                card_brand=card_data.get('brand', 'Visa'),
                amount_paid=reservation.total_amount,
                paid_at=timezone.now()
            )
            
            # Update reservation status
            old_status = reservation.status
            reservation.status = 'confirmed'
            reservation.payment_status = 'paid'
            reservation.save()
            
            # Create status history record
            from .models import ReservationStatusHistory
            ReservationStatusHistory.objects.create(
                reservation=reservation,
                old_status=old_status,
                new_status='confirmed',
                changed_by=request.user,
                reason='Payment processed successfully'
            )
            
            return Response({
                'message': 'Reservation confirmed successfully',
                'reservation_id': str(reservation.id),
                'confirmation_number': reservation.confirmation_number,
                'payment': ReservationPaymentSerializer(payment).data
            })
            
        except Reservation.DoesNotExist:
            return Response(
                {'error': 'Reservation not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_reservation_history(request):
    """
    Get reservation history for the current user
    """
    user = request.user
    reservations = Reservation.objects.filter(user=user).order_by('-created_at')
    
    # Optional filtering
    status_filter = request.GET.get('status')
    if status_filter:
        reservations = reservations.filter(status=status_filter)
    
    year = request.GET.get('year')
    if year:
        try:
            year = int(year)
            reservations = reservations.filter(created_at__year=year)
        except ValueError:
            pass
    
    serializer = ReservationListSerializer(reservations, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def landlord_reservations(request):
    """
    Get reservations for properties owned by the current user (landlord view)
    """
    user = request.user
    
    # Get reservations for listings owned by this user
    reservations = Reservation.objects.filter(
        listing__owner=user
    ).order_by('-created_at')
    
    # Optional filtering
    status_filter = request.GET.get('status')
    if status_filter:
        reservations = reservations.filter(status=status_filter)
    
    listing_id = request.GET.get('listing_id')
    if listing_id:
        reservations = reservations.filter(listing_id=listing_id)
    
    serializer = ReservationListSerializer(reservations, many=True)
    return Response(serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class AvailabilityBlockListCreateView(generics.ListCreateAPIView):
    """
    List and create availability blocks (for landlords to block dates)
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AvailabilityBlockSerializer
    
    def get_queryset(self):
        user = self.request.user
        # Only show blocks for listings owned by the user
        return AvailabilityBlock.objects.filter(listing__owner=user)
    
    def perform_create(self, serializer):
        # Ensure the listing belongs to the current user
        listing = serializer.validated_data['listing']
        if listing.owner != self.request.user:
            raise serializers.ValidationError("You can only create blocks for your own listings")
        serializer.save()


# Booking flow endpoints matching frontend steps
@method_decorator(csrf_exempt, name='dispatch')
class BookingStepOneView(APIView):
    """
    Step 1: Validate guest information and check availability
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        # Extract and validate guest info
        guest_data = {
            'guest_first_name': request.data.get('firstName'),
            'guest_last_name': request.data.get('lastName'),
            'guest_email': request.data.get('email'),
            'guest_phone': request.data.get('phone'),
            'special_requests': request.data.get('specialRequests', ''),
        }
        
        booking_data = {
            'listing_id': request.data.get('listing_id'),
            'check_in': request.data.get('check_in'),
            'check_out': request.data.get('check_out'),
            'guests_adults': request.data.get('guests_adults', 1),
            'guests_children': request.data.get('guests_children', 0),
        }
        
        # Validate the data
        create_serializer = ReservationCreateSerializer(
            data={**guest_data, **booking_data, 'payment_method': 'card'},
            context={'request': request}
        )
        
        if create_serializer.is_valid():
            # Store in session or return for frontend to use in step 2
            return Response({
                'valid': True,
                'guest_data': guest_data,
                'booking_data': booking_data,
                'message': 'Guest information validated successfully'
            })
        
        return Response({
            'valid': False,
            'errors': create_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class BookingStepTwoView(APIView):
    """
    Step 2: Process payment information
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        payment_method = request.data.get('payment_method')
        card_data = request.data.get('card_details', {})
        
        # Validate payment method
        if payment_method not in ['card', 'paypal']:
            return Response({
                'valid': False,
                'errors': {'payment_method': ['Invalid payment method']}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # For card payments, validate card data
        if payment_method == 'card':
            required_fields = ['number', 'expiry', 'cvv', 'name']
            for field in required_fields:
                if not card_data.get(field):
                    return Response({
                        'valid': False,
                        'errors': {'card_details': [f'{field} is required']}
                    }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'valid': True,
            'payment_method': payment_method,
            'message': 'Payment information validated successfully'
        })


@method_decorator(csrf_exempt, name='dispatch')
class BookingStepThreeView(APIView):
    """
    Step 3: Final confirmation and reservation creation
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        # Get all booking data from the request
        serializer = ReservationCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            # Create the reservation
            reservation = serializer.save()
            
            # Return detailed reservation data
            detail_serializer = ReservationDetailSerializer(reservation)
            return Response({
                'success': True,
                'reservation': detail_serializer.data,
                'message': 'Reservation created successfully'
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

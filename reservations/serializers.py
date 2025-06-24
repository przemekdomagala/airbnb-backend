from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from listings.serializers import ListingSerializer
from .models import (
    Reservation, ReservationPayment, ReservationNote, 
    ReservationStatusHistory, AvailabilityBlock
)

User = get_user_model()


class ReservationUserSerializer(serializers.ModelSerializer):
    """Simplified user serializer for reservations"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class ReservationPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationPayment
        fields = [
            'id', 'payment_provider', 'card_last_four', 'card_brand', 
            'amount_paid', 'currency', 'paid_at', 'refunded_at'
        ]
        read_only_fields = ['id', 'paid_at', 'refunded_at']


class ReservationNoteSerializer(serializers.ModelSerializer):
    author = ReservationUserSerializer(read_only=True)
    
    class Meta:
        model = ReservationNote
        fields = ['id', 'note', 'is_internal', 'created_at', 'author']
        read_only_fields = ['id', 'created_at', 'author']


class ReservationStatusHistorySerializer(serializers.ModelSerializer):
    changed_by = ReservationUserSerializer(read_only=True)
    
    class Meta:
        model = ReservationStatusHistory
        fields = ['id', 'old_status', 'new_status', 'reason', 'changed_at', 'changed_by']
        read_only_fields = ['id', 'changed_at', 'changed_by']


class ReservationListSerializer(serializers.ModelSerializer):
    """Serializer for listing reservations (less detailed)"""
    user = ReservationUserSerializer(read_only=True)
    listing_title = serializers.CharField(source='listing.title', read_only=True)
    listing_location = serializers.CharField(source='listing.location', read_only=True)
    guest_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Reservation
        fields = [
            'id', 'confirmation_number', 'user', 'listing_title', 'listing_location',
            'check_in', 'check_out', 'total_nights', 'guest_name', 'guests_adults', 
            'guests_children', 'total_amount', 'status', 'payment_status', 'created_at'
        ]
    
    def get_guest_name(self, obj):
        return f"{obj.guest_first_name} {obj.guest_last_name}"


class ReservationDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for individual reservation"""
    user = ReservationUserSerializer(read_only=True)
    listing = ListingSerializer(read_only=True)
    payment = ReservationPaymentSerializer(read_only=True)
    notes = ReservationNoteSerializer(many=True, read_only=True)
    status_history = ReservationStatusHistorySerializer(many=True, read_only=True)
    guest_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Reservation
        fields = [
            'id', 'confirmation_number', 'user', 'listing', 'check_in', 'check_out',
            'guests_adults', 'guests_children', 'total_nights', 'guest_first_name',
            'guest_last_name', 'guest_name', 'guest_email', 'guest_phone', 
            'special_requests', 'price_per_night', 'subtotal', 'taxes_and_fees',
            'total_amount', 'status', 'payment_status', 'payment_method',
            'created_at', 'updated_at', 'payment', 'notes', 'status_history'
        ]
        read_only_fields = [
            'id', 'confirmation_number', 'total_nights', 'created_at', 'updated_at'
        ]
    
    def get_guest_name(self, obj):
        return f"{obj.guest_first_name} {obj.guest_last_name}"


class ReservationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new reservations (3-step booking process)"""
    listing_id = serializers.CharField(write_only=True)
    
    # Step 1: Guest Information
    guest_first_name = serializers.CharField(max_length=100)
    guest_last_name = serializers.CharField(max_length=100)
    guest_email = serializers.EmailField()
    guest_phone = serializers.CharField(max_length=20)
    special_requests = serializers.CharField(required=False, allow_blank=True)
    
    # Step 2: Payment Information
    payment_method = serializers.ChoiceField(choices=[('card', 'Card'), ('paypal', 'PayPal')])
    
    # Step 3: Booking Details
    check_in = serializers.DateField()
    check_out = serializers.DateField()
    guests_adults = serializers.IntegerField(min_value=1)
    guests_children = serializers.IntegerField(min_value=0, default=0)
    
    class Meta:
        model = Reservation
        fields = [
            'listing_id', 'check_in', 'check_out', 'guests_adults', 'guests_children',
            'guest_first_name', 'guest_last_name', 'guest_email', 'guest_phone',
            'special_requests', 'payment_method'        ]
    
    def validate(self, data):
        """Validate booking data"""
        check_in = data.get('check_in')
        check_out = data.get('check_out')
        
        if check_in and check_out:
            if check_in >= check_out:
                raise serializers.ValidationError("Check-out date must be after check-in date")
            today = timezone.now().date()
            if check_in < today:
                raise serializers.ValidationError("Check-in date cannot be in the past")
        
        return data
    
    def create(self, validated_data):
        from listings.models import Listing
          # Extract listing
        listing_id = validated_data.pop('listing_id')
        
        # Handle both numeric IDs and string slugs
        if isinstance(listing_id, str) and not listing_id.isdigit():            # Map known hotel slugs to IDs
            HOTEL_SLUG_MAP = {
                'grand-plaza': 1,  # Urban retreat with city skyline views
                'luxury-suite': 2, # Contemporary villa with garden  
                'cozy-apartment': 3, # Cozy apartment in the heart of the city
                'modern-loft': 11, # Modern loft with stunning views
                'seaside-villa': 9, # Spacious family home near the beach
                'urban-retreat': 1,
                'contemporary-villa': 2,
                'stylish-condo': 6,
                'luxury-penthouse': 13,
                'waterfront-cottage': 10,
            }
            
            if listing_id in HOTEL_SLUG_MAP:
                listing_id = HOTEL_SLUG_MAP[listing_id]
            else:
                raise serializers.ValidationError({
                    "listing_id": f"Unknown hotel slug '{listing_id}'. Available options: {', '.join(HOTEL_SLUG_MAP.keys())}"
                })
        
        # Validate and convert listing_id to integer
        try:
            listing_id = int(listing_id)
        except (ValueError, TypeError):
            raise serializers.ValidationError({
                "listing_id": f"Invalid listing ID '{listing_id}'. Expected a numeric value or valid hotel slug."
            })
        
        try:
            listing = Listing.objects.get(id=listing_id)
        except Listing.DoesNotExist:
            raise serializers.ValidationError({
                "listing_id": f"Listing with ID {listing_id} not found."
            })
        
        # Calculate pricing
        check_in = validated_data['check_in']
        check_out = validated_data['check_out']
        
        from decimal import Decimal
        
        total_nights = (check_out - check_in).days
        price_per_night = listing.price_per_night
        subtotal = price_per_night * total_nights
        taxes_and_fees = subtotal * Decimal('0.15')  # 15% taxes and fees
        total_amount = subtotal + taxes_and_fees
        
        # Create reservation
        reservation = Reservation.objects.create(
            user=self.context['request'].user,
            listing=listing,
            total_nights=total_nights,
            price_per_night=price_per_night,
            subtotal=subtotal,
            taxes_and_fees=taxes_and_fees,
            total_amount=total_amount,
            **validated_data
        )
        
        # Create availability block
        AvailabilityBlock.objects.create(
            listing=listing,
            start_date=check_in,
            end_date=check_out,
            reservation=reservation
        )
        
        return reservation


class AvailabilityCheckSerializer(serializers.Serializer):
    """Serializer for checking listing availability"""
    listing_id = serializers.CharField()
    check_in = serializers.DateField()
    check_out = serializers.DateField()
    
    def validate(self, data):
        check_in = data.get('check_in')
        check_out = data.get('check_out')
        
        if check_in >= check_out:
            raise serializers.ValidationError("Check-out date must be after check-in date")
        
        return data


class AvailabilityBlockSerializer(serializers.ModelSerializer):
    listing_title = serializers.CharField(source='listing.title', read_only=True)
    
    class Meta:
        model = AvailabilityBlock
        fields = [
            'id', 'listing', 'listing_title', 'start_date', 'end_date',
            'is_blocked', 'block_reason', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

from rest_framework import serializers
from .models import (
    Listing, Advertisement, AdvertisementCategory, PropertyImages,
    RentalAdvertisement, HotelAdvertisement, HotelRoom, 
    AdvertisementPricing, AdvertisementStatistics
)


class ListingSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Listing
        fields = [
            "id",
            "title",
            "description",
            "price_per_night",
            "location",
            "latitude",
            "longitude",
            "image_url",
            "created_at",
            "owner",
            "owner_username",
        ]
        read_only_fields = ["owner"]


class AdvertisementCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementCategory
        fields = ['id', 'name', 'description', 'created_at']


class PropertyImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImages
        fields = ['id', 'image_url', 'alt_text', 'is_primary', 'upload_date']


class AdvertisementPricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementPricing
        fields = ['base_price', 'currency', 'weekend_multiplier', 'cleaning_fee', 'service_fee', 'tax_rate']


class AdvertisementStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementStatistics
        fields = ['view_count', 'click_count', 'share_count', 'favorite_count', 'inquiry_count', 'booking_count']


class RentalAdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalAdvertisement
        fields = ['price_per_night', 'minimum_stay', 'maximum_stay', 'instant_booking', 
                 'check_in_time', 'check_out_time', 'house_rules']


class HotelRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelRoom
        fields = ['id', 'room_type', 'room_name', 'price_per_night', 'max_occupancy', 
                 'total_rooms', 'room_size_sqm', 'has_balcony', 'has_sea_view', 'has_city_view', 'has_kitchenette']


class HotelAdvertisementSerializer(serializers.ModelSerializer):
    rooms = HotelRoomSerializer(many=True, read_only=True)

    class Meta:
        model = HotelAdvertisement
        fields = ['hotel_name', 'hotel_chain', 'star_rating', 'has_restaurant', 
                 'has_spa', 'has_gym', 'has_pool', 'has_business_center', 'rooms']


class AdvertisementSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    user_username = serializers.ReadOnlyField(source='user.username')
    images = PropertyImagesSerializer(many=True, read_only=True)
    pricing = AdvertisementPricingSerializer(many=True, read_only=True)
    statistics = AdvertisementStatisticsSerializer(read_only=True)
    
    # Related data based on advertisement type
    rental_details = RentalAdvertisementSerializer(source='rentaladvertisement', read_only=True)
    hotel_details = HotelAdvertisementSerializer(source='hoteladvertisement', read_only=True)
    
    # Write-only fields for creating related objects
    rental_data = serializers.DictField(write_only=True, required=False)
    hotel_data = serializers.DictField(write_only=True, required=False)

    class Meta:
        model = Advertisement
        fields = [
            'advertisement_id', 'title', 'description', 'advertisement_type', 
            'category', 'category_name', 'user', 'user_username', 'location', 
            'latitude', 'longitude', 'status', 'created_at', 'updated_at',
            'max_guests', 'bedrooms', 'bathrooms', 'images', 'pricing', 'statistics',
            'rental_details', 'hotel_details', 'rental_data', 'hotel_data'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Extract nested data
        rental_data = validated_data.pop('rental_data', None)
        hotel_data = validated_data.pop('hotel_data', None)
        
        # Create the main Advertisement object
        advertisement = Advertisement.objects.create(**validated_data)
        
        # Create related objects based on type
        if advertisement.advertisement_type == 'private' and rental_data:
            RentalAdvertisement.objects.create(
                advertisement=advertisement,
                **rental_data
            )
        elif advertisement.advertisement_type == 'hotel' and hotel_data:
            HotelAdvertisement.objects.create(
                advertisement=advertisement,
                **hotel_data
            )
        
        return advertisement
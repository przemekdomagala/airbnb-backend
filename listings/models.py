from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal


# Core Advertisement Models
class AdvertisementCategory(models.Model):
    """Represents different categories of advertisements (Hotels, Private Rentals, etc.)"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Advertisement Categories"

    def __str__(self):
        return self.name


class Advertisement(models.Model):
    """Base advertisement model - represents both private listings and hotels"""
    ADVERTISEMENT_TYPES = [
        ('private', 'Private Listing'),
        ('hotel', 'Hotel'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ]

    # Core fields
    advertisement_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    advertisement_type = models.CharField(max_length=20, choices=ADVERTISEMENT_TYPES)
    category = models.ForeignKey(AdvertisementCategory, on_delete=models.CASCADE)
      # User and property reference
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="advertisements", null=True, blank=True)
    
    # Location details
    location = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Status and metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Accommodation details
    max_guests = models.PositiveIntegerField(default=1)
    bedrooms = models.PositiveIntegerField(default=1)
    bathrooms = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.title} ({self.get_advertisement_type_display()})"


class PropertyImages(models.Model):
    """Manages images for advertisements"""
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField(max_length=500)
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    upload_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', 'upload_date']

    def __str__(self):
        return f"Image for {self.advertisement.title}"


# Specialized Advertisement Types
class RentalAdvertisement(models.Model):
    """Represents short-term rental advertisements (private listings)"""
    advertisement = models.OneToOneField(Advertisement, on_delete=models.CASCADE, primary_key=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_stay = models.PositiveIntegerField(default=1, help_text="Minimum nights")
    maximum_stay = models.PositiveIntegerField(null=True, blank=True, help_text="Maximum nights")
    
    # Rental specific features
    instant_booking = models.BooleanField(default=False)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    house_rules = models.TextField(blank=True)

    def __str__(self):
        return f"Rental: {self.advertisement.title}"


class HotelAdvertisement(models.Model):
    """Represents hotel advertisements with room-based pricing"""
    advertisement = models.OneToOneField(Advertisement, on_delete=models.CASCADE, primary_key=True)
    
    # Hotel specific details
    hotel_name = models.CharField(max_length=200)
    hotel_chain = models.CharField(max_length=100, blank=True)
    star_rating = models.PositiveIntegerField(choices=[(i, f"{i} Star") for i in range(1, 6)], null=True, blank=True)
    
    # Services
    has_restaurant = models.BooleanField(default=False)
    has_spa = models.BooleanField(default=False)
    has_gym = models.BooleanField(default=False)
    has_pool = models.BooleanField(default=False)
    has_business_center = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Hotel: {self.hotel_name}"


class HotelRoom(models.Model):
    """Represents individual room types in a hotel"""
    ROOM_TYPES = [
        ('standard', 'Standard Room'),
        ('deluxe', 'Deluxe Room'),
        ('suite', 'Suite'),
        ('presidential', 'Presidential Suite'),
    ]
    
    hotel = models.ForeignKey(HotelAdvertisement, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    room_name = models.CharField(max_length=100)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    max_occupancy = models.PositiveIntegerField()
    total_rooms = models.PositiveIntegerField()
    room_size_sqm = models.PositiveIntegerField(null=True, blank=True)
      # Room amenities
    has_balcony = models.BooleanField(default=False)
    has_sea_view = models.BooleanField(default=False)
    has_city_view = models.BooleanField(default=False)
    has_kitchenette = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.hotel.hotel_name} - {self.room_name}"


# Advertisement Enhancement Models
class PremiumAdvertisement(models.Model):
    """Represents premium features for advertisements"""
    advertisement = models.OneToOneField(Advertisement, on_delete=models.CASCADE, primary_key=True)
    is_featured = models.BooleanField(default=False)
    feature_start_date = models.DateTimeField(null=True, blank=True)
    feature_end_date = models.DateTimeField(null=True, blank=True)
    boost_priority = models.PositiveIntegerField(default=0, help_text="Higher number = higher priority")
    premium_badge = models.BooleanField(default=False)

    def __str__(self):
        return f"Premium: {self.advertisement.title}"

    @property
    def is_currently_featured(self):
        now = timezone.now()
        if not self.is_featured:
            return False
        if self.feature_start_date and now < self.feature_start_date:
            return False
        if self.feature_end_date and now > self.feature_end_date:
            return False
        return True


class SeasonalAdvertisement(models.Model):
    """Represents seasonal pricing and availability"""
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='seasonal_info')
    season_name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    price_multiplier = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('1.00'))
    minimum_stay_override = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ['advertisement', 'season_name', 'start_date']

    def __str__(self):
        return f"{self.advertisement.title} - {self.season_name}"


class AdvertisementTag(models.Model):
    """Tags for categorizing and searching advertisements"""
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='tags')
    tag_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['advertisement', 'tag_name']

    def __str__(self):
        return f"{self.advertisement.title} - {self.tag_name}"


class AdvertisementPricing(models.Model):
    """Manages different pricing strategies"""
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('PLN', 'Polish Zloty'),
        ('GBP', 'British Pound'),
    ]

    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='pricing')
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    weekend_multiplier = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('1.00'))
    cleaning_fee = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    service_fee = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    tax_rate = models.DecimalField(max_digits=5, decimal_places=4, default=Decimal('0.00'))

    def __str__(self):
        return f"Pricing for {self.advertisement.title}"


class AdvertisementStatistics(models.Model):
    """Tracks advertisement performance metrics"""
    advertisement = models.OneToOneField(Advertisement, on_delete=models.CASCADE, primary_key=True)
    view_count = models.PositiveIntegerField(default=0)
    click_count = models.PositiveIntegerField(default=0)
    share_count = models.PositiveIntegerField(default=0)
    favorite_count = models.PositiveIntegerField(default=0)
    inquiry_count = models.PositiveIntegerField(default=0)
    booking_count = models.PositiveIntegerField(default=0)
    last_viewed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Stats: {self.advertisement.title}"


class AdvertisementSchedule(models.Model):
    """Manages publication and expiration scheduling"""
    advertisement = models.OneToOneField(Advertisement, on_delete=models.CASCADE, primary_key=True)
    publish_date = models.DateTimeField()
    expiration_date = models.DateTimeField(null=True, blank=True)
    auto_renew = models.BooleanField(default=False)
    renewal_period_days = models.PositiveIntegerField(default=30)

    def __str__(self):
        return f"Schedule: {self.advertisement.title}"

    @property
    def is_published(self):
        now = timezone.now()
        return now >= self.publish_date

    @property
    def is_expired(self):
        if not self.expiration_date:
            return False
        return timezone.now() > self.expiration_date


class AdvertisementReport(models.Model):
    """Handles user reports on advertisements"""
    REPORT_REASONS = [
        ('inappropriate', 'Inappropriate Content'),
        ('misleading', 'Misleading Information'),
        ('spam', 'Spam'),
        ('duplicate', 'Duplicate Listing'),
        ('fraud', 'Fraudulent Activity'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]

    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.CharField(max_length=20, choices=REPORT_REASONS)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Report: {self.advertisement.title} - {self.get_reason_display()}"


# Legacy model for backward compatibility
class Listing(models.Model):
    """Legacy listing model - maintained for backward compatibility"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    image_url = models.URLField(max_length=500, null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="listings")

    def __str__(self):
        return self.title

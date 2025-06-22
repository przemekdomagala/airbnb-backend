from django.contrib import admin
from .models import (
    Listing, Advertisement, AdvertisementCategory, PropertyImages,
    RentalAdvertisement, HotelAdvertisement, HotelRoom, PremiumAdvertisement,
    SeasonalAdvertisement, AdvertisementTag, AdvertisementPricing,
    AdvertisementStatistics, AdvertisementSchedule, AdvertisementReport
)


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "location", "price_per_night", "created_at")
    search_fields = ("title", "location", "owner__username")
    list_filter = ("location", "created_at")


@admin.register(AdvertisementCategory)
class AdvertisementCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at")
    search_fields = ("name",)


class PropertyImagesInline(admin.TabularInline):
    model = PropertyImages
    extra = 1


class AdvertisementPricingInline(admin.TabularInline):
    model = AdvertisementPricing
    extra = 0


class AdvertisementTagInline(admin.TabularInline):
    model = AdvertisementTag
    extra = 1


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ("title", "advertisement_type", "category", "user", "status", "location", "created_at")
    search_fields = ("title", "location", "user__username")
    list_filter = ("advertisement_type", "category", "status", "created_at")
    inlines = [PropertyImagesInline, AdvertisementPricingInline, AdvertisementTagInline]
    readonly_fields = ("created_at", "updated_at")


@admin.register(RentalAdvertisement)
class RentalAdvertisementAdmin(admin.ModelAdmin):
    list_display = ("advertisement", "price_per_night", "minimum_stay", "instant_booking")
    search_fields = ("advertisement__title",)
    list_filter = ("instant_booking", "minimum_stay")


class HotelRoomInline(admin.TabularInline):
    model = HotelRoom
    extra = 1


@admin.register(HotelAdvertisement)
class HotelAdvertisementAdmin(admin.ModelAdmin):
    list_display = ("hotel_name", "star_rating", "has_restaurant", "has_spa", "has_pool")
    search_fields = ("hotel_name", "hotel_chain")
    list_filter = ("star_rating", "has_restaurant", "has_spa", "has_gym", "has_pool")
    inlines = [HotelRoomInline]


@admin.register(HotelRoom)
class HotelRoomAdmin(admin.ModelAdmin):
    list_display = ("hotel", "room_name", "room_type", "price_per_night", "max_occupancy", "total_rooms")
    search_fields = ("hotel__hotel_name", "room_name")
    list_filter = ("room_type", "has_balcony", "has_sea_view", "has_city_view")


@admin.register(PremiumAdvertisement)
class PremiumAdvertisementAdmin(admin.ModelAdmin):
    list_display = ("advertisement", "is_featured", "feature_start_date", "feature_end_date", "boost_priority")
    search_fields = ("advertisement__title",)
    list_filter = ("is_featured", "premium_badge", "feature_start_date")


@admin.register(AdvertisementStatistics)
class AdvertisementStatisticsAdmin(admin.ModelAdmin):
    list_display = ("advertisement", "view_count", "click_count", "favorite_count", "booking_count")
    search_fields = ("advertisement__title",)
    readonly_fields = ("view_count", "click_count", "share_count", "favorite_count", "inquiry_count", "booking_count")


@admin.register(AdvertisementReport)
class AdvertisementReportAdmin(admin.ModelAdmin):
    list_display = ("advertisement", "reporter", "reason", "status", "created_at")
    search_fields = ("advertisement__title", "reporter__username")
    list_filter = ("reason", "status", "created_at")
    readonly_fields = ("created_at", "resolved_at")

from django.contrib import admin
from .models import (
    Reservation, ReservationPayment, ReservationNote, 
    ReservationStatusHistory, AvailabilityBlock
)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = [
        'confirmation_number', 'guest_name', 'listing', 'check_in', 'check_out', 
        'total_nights', 'total_amount', 'status', 'payment_status', 'created_at'
    ]
    list_filter = ['status', 'payment_status', 'created_at', 'check_in']
    search_fields = [
        'confirmation_number', 'guest_first_name', 'guest_last_name', 
        'guest_email', 'listing__title', 'user__username'
    ]
    readonly_fields = ['id', 'confirmation_number', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'confirmation_number', 'user', 'listing', 'status', 'payment_status')
        }),
        ('Guest Information', {
            'fields': ('guest_first_name', 'guest_last_name', 'guest_email', 'guest_phone', 'special_requests')
        }),
        ('Booking Details', {
            'fields': ('check_in', 'check_out', 'total_nights', 'guests_adults', 'guests_children')
        }),
        ('Pricing', {
            'fields': ('price_per_night', 'subtotal', 'taxes_and_fees', 'total_amount')
        }),
        ('Payment', {
            'fields': ('payment_method',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def guest_name(self, obj):
        return f"{obj.guest_first_name} {obj.guest_last_name}"
    guest_name.short_description = 'Guest Name'


@admin.register(ReservationPayment)
class ReservationPaymentAdmin(admin.ModelAdmin):
    list_display = [
        'reservation', 'payment_provider', 'amount_paid', 'currency', 
        'card_last_four', 'paid_at', 'created_at'
    ]
    list_filter = ['payment_provider', 'currency', 'paid_at']
    search_fields = ['reservation__confirmation_number', 'payment_intent_id']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ReservationNote)
class ReservationNoteAdmin(admin.ModelAdmin):
    list_display = ['reservation', 'author', 'is_internal', 'created_at']
    list_filter = ['is_internal', 'created_at']
    search_fields = ['reservation__confirmation_number', 'note', 'author__username']
    readonly_fields = ['created_at']


@admin.register(ReservationStatusHistory)
class ReservationStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ['reservation', 'old_status', 'new_status', 'changed_by', 'changed_at']
    list_filter = ['old_status', 'new_status', 'changed_at']
    search_fields = ['reservation__confirmation_number', 'reason']
    readonly_fields = ['changed_at']


@admin.register(AvailabilityBlock)
class AvailabilityBlockAdmin(admin.ModelAdmin):
    list_display = [
        'listing', 'start_date', 'end_date', 'reservation', 
        'is_blocked', 'block_reason', 'created_at'
    ]
    list_filter = ['is_blocked', 'start_date', 'created_at']
    search_fields = ['listing__title', 'block_reason', 'reservation__confirmation_number']
    readonly_fields = ['created_at']
    date_hierarchy = 'start_date'

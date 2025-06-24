from django.db import models
from django.conf import settings
from listings.models import Listing
import uuid


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
        ('failed', 'Failed'),
    ]

    # Basic reservation info
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    confirmation_number = models.CharField(max_length=20, unique=True, blank=True)
    
    # Relations
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reservations')
    
    # Dates and guests
    check_in = models.DateField()
    check_out = models.DateField()
    guests_adults = models.PositiveIntegerField(default=1)
    guests_children = models.PositiveIntegerField(default=0)
    total_nights = models.PositiveIntegerField()
    
    # Guest information (from step 1 of booking)
    guest_first_name = models.CharField(max_length=100)
    guest_last_name = models.CharField(max_length=100)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=20)
    special_requests = models.TextField(blank=True, null=True)
    
    # Pricing
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    taxes_and_fees = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Status and timestamps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Payment method info (from step 2)
    payment_method = models.CharField(max_length=20, choices=[('card', 'Card'), ('paypal', 'PayPal')], default='card')
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['listing', 'check_in', 'check_out']),
            models.Index(fields=['confirmation_number']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.confirmation_number:
            self.confirmation_number = self.generate_confirmation_number()
        if not self.total_nights:
            self.total_nights = (self.check_out - self.check_in).days
        super().save(*args, **kwargs)
    
    def generate_confirmation_number(self):
        import random
        import string
        return 'DB' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    def __str__(self):
        return f"Reservation {self.confirmation_number} - {self.guest_first_name} {self.guest_last_name}"


class ReservationPayment(models.Model):
    """Payment details for reservations"""
    PAYMENT_PROVIDER_CHOICES = [
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        ('blik', 'BLIK'),
    ]
    
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='payment')
    payment_intent_id = models.CharField(max_length=200, blank=True, null=True)
    payment_provider = models.CharField(max_length=20, choices=PAYMENT_PROVIDER_CHOICES, default='stripe')
    
    # Card info (masked for security)
    card_last_four = models.CharField(max_length=4, blank=True, null=True)
    card_brand = models.CharField(max_length=20, blank=True, null=True)
    
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default='PLN')
    paid_at = models.DateTimeField(null=True, blank=True)
    refunded_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Payment for {self.reservation.confirmation_number}"


class ReservationNote(models.Model):
    """Internal notes for reservations"""
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='notes')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    note = models.TextField()
    is_internal = models.BooleanField(default=True)  # False if visible to guest
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Note for {self.reservation.confirmation_number}"


class ReservationStatusHistory(models.Model):
    """Track status changes for reservations"""
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='status_history')
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.TextField(blank=True, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-changed_at']
        verbose_name_plural = "Reservation status histories"
    
    def __str__(self):
        return f"{self.reservation.confirmation_number}: {self.old_status} → {self.new_status}"


class AvailabilityBlock(models.Model):
    """Track availability blocks to prevent double bookings"""
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='availability_blocks')
    start_date = models.DateField()
    end_date = models.DateField()
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, null=True, blank=True)
    is_blocked = models.BooleanField(default=False)  # Manual block by host
    block_reason = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['start_date']
        indexes = [
            models.Index(fields=['listing', 'start_date', 'end_date']),
        ]
    
    def __str__(self):
        return f"{self.listing.title}: {self.start_date} - {self.end_date}"

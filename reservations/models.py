from django.db import models
from django.conf import settings
from django.utils import timezone

class Property(models.Model):
    title = models.CharField(max_length=200)
    address = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class CancellationPolicy(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    refundable_until = models.DurationField()

class SpecialOffer(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

class GroupReservation(models.Model):
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='group_participants')
    created_at = models.DateTimeField(auto_now_add=True)

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    group = models.ForeignKey(GroupReservation, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class ReservationDiscount(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    offer = models.ForeignKey(SpecialOffer, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)

class ReservationInvoice(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    issued_at = models.DateTimeField(auto_now_add=True)

class ReservationPayment(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=255)
    status = models.CharField(max_length=20)
    paid_at = models.DateTimeField(null=True, blank=True)

class ReservationNotification(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

class ReservationReminder(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    remind_at = models.DateTimeField()
    sent = models.BooleanField(default=False)

class ReservationExtension(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    new_end_date = models.DateField()
    requested_at = models.DateTimeField(auto_now_add=True)

class ReservationModification(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    changes = models.JSONField()
    modified_at = models.DateTimeField(auto_now_add=True)

class ReservationSupportTicket(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

# Reporting and analytics
class ReservationOccupancy(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    date = models.DateField()
    occupancy_count = models.PositiveIntegerField()

class RevenueReport(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    period_start = models.DateField()
    period_end = models.DateField()
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)

class UserActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

class UserNotificationPreferences(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
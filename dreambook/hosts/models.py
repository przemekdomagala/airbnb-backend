# hosts/models.py
from django.db import models

class Host(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    rating = models.FloatField(default=0.0)
    image = models.URLField()

    def __str__(self):
        return f"{self.name} ({self.location})"

class HostAvailability(models.Model):
    host = models.ForeignKey('Host', on_delete=models.CASCADE, related_name='availabilities')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.host.name}: {self.start_date} – {self.end_date}"
    
class HostBooking(models.Model):
    host = models.ForeignKey('Host', on_delete=models.CASCADE, related_name='bookings')
    reservation_id = models.IntegerField()
    booking_date = models.DateField()

    def __str__(self):
        return f"Booking {self.reservation_id} for {self.host.name} on {self.booking_date}"
    
class HostMessage(models.Model):
    host = models.ForeignKey('Host', on_delete=models.CASCADE, related_name='messages')
    user_id = models.IntegerField()
    message_text = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Msg to {self.user_id} from {self.host.name}"
    
class HostPromotion(models.Model):
    host = models.ForeignKey('Host', on_delete=models.CASCADE, related_name='promotions')
    promotion_details = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Promotion for {self.host.name}: {self.start_date} – {self.end_date}"

class HostStatistics(models.Model):
    host = models.OneToOneField('Host', on_delete=models.CASCADE, related_name='statistics')
    total_reservations = models.IntegerField(default=0)
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Stats for {self.host.name}"

class HostEarnings(models.Model):
    host = models.ForeignKey('Host', on_delete=models.CASCADE, related_name='earnings')
    earnings_amount = models.DecimalField(max_digits=10, decimal_places=2)
    earnings_date = models.DateField()

    def __str__(self):
        return f"{self.host.name}: {self.earnings_amount} zł on {self.earnings_date}"

class HostReservationPolicy(models.Model):
    host = models.OneToOneField('Host', on_delete=models.CASCADE, related_name='reservation_policy')
    cancellation_policy = models.TextField()

    def __str__(self):
        return f"Policy for {self.host.name}"

class HostNotification(models.Model):
    host = models.ForeignKey('Host', on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=100)
    notification_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.notification_type} → {self.host.name}"

class HostSupport(models.Model):
    STATUS_CHOICES = [
        ('new', 'Nowe'),
        ('in_progress', 'W trakcie'),
        ('closed', 'Zamknięte'),
    ]

    host = models.ForeignKey('Host', on_delete=models.CASCADE, related_name='support_tickets')
    issue_description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    def __str__(self):
        return f"Support for {self.host.name} – {self.status}"

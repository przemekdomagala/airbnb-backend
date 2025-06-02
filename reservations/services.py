from .models import Reservation, Property, ReservationReminder, SpecialOffer
from django.db.models import Q
from django.utils import timezone
from django.core.mail import send_mail

class AvailabilityChecker:
    @staticmethod
    def is_available(property_id, start_date, end_date):
        overlaps = Reservation.objects.filter(
            property_id=property_id,
            status='confirmed',
            start_date__lt=end_date,
            end_date__gt=start_date
        )
        return not overlaps.exists()

class NotificationService:
    @staticmethod
    def send_reservation_email(reservation, subject, message):
        send_mail(subject, message, 'no-reply@example.com', [reservation.user.email])
        # record
        from .models import ReservationNotification
        ReservationNotification.objects.create(reservation=reservation, message=message)

class ReservationHistoryService:
    @staticmethod
    def get_user_reservation_history(user_id):
        """
        Retrieve reservation history for a specific user
        """
        return Reservation.objects.filter(
            user_id=user_id
        ).order_by('-created_at')
        
    @staticmethod
    def get_property_reservation_history(property_id):
        """
        Retrieve reservation history for a specific property
        """
        return Reservation.objects.filter(
            property_id=property_id
        ).order_by('-created_at')

class ReservationConfirmationService:
    @staticmethod
    def process_payment(reservation, payment_data):
        # Integracja z Stripe / BLIK etc.
        # TODO: implement actual call
        from .models import ReservationPayment
        return ReservationPayment.objects.create(
            reservation=reservation,
            payment_id='STRIPE_FAKE_ID',
            status='paid',
            paid_at=timezone.now()
        )

class InvoiceService:
    @staticmethod
    def generate_invoice(reservation):
        # TODO: wygeneruj PDF, zapisz ścieżkę
        from .models import ReservationInvoice
        amount = reservation.property.price * (reservation.end_date - reservation.start_date).days
        return ReservationInvoice.objects.create(reservation=reservation, amount=amount)

class ReportingService:
    @staticmethod
    def occupancy_report(property_id, date):
        from .models import ReservationOccupancy
        return ReservationOccupancy.objects.filter(property_id=property_id, date=date).first()

class AnalyticsService:
    @staticmethod
    def revenue_summary(property_id, start_date, end_date):
        from .models import RevenueReport
        return RevenueReport.objects.filter(property_id=property_id,
            period_start__gte=start_date, period_end__lte=end_date)

class ReminderScheduler:
    @staticmethod
    def schedule_reminders():
        now = timezone.now()
        due = ReservationReminder.objects.filter(remind_at__lte=now, sent=False)
        for reminder in due:
            NotificationService.send_reservation_email(
                reminder.reservation,
                'Przypomnienie o rezerwacji',
                f'Przypominamy o rezerwacji {reminder.reservation.id}.'
            )
            reminder.sent = True
            reminder.save()
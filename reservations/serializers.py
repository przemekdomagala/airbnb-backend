from rest_framework import serializers
from .models import (
    Property, CancellationPolicy, SpecialOffer, GroupReservation, Reservation,
    ReservationDiscount, ReservationInvoice, ReservationPayment, ReservationNotification,
    ReservationReminder, ReservationExtension, ReservationModification, ReservationSupportTicket,
    ReservationOccupancy, RevenueReport, UserActivity, UserNotificationPreferences
)

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class CancellationPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = CancellationPolicy
        fields = '__all__'

class SpecialOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialOffer
        fields = '__all__'

class GroupReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupReservation
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class ReservationDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationDiscount
        fields = '__all__'

class ReservationInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationInvoice
        fields = '__all__'

class ReservationPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationPayment
        fields = '__all__'

class ReservationNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationNotification
        fields = '__all__'

class ReservationReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationReminder
        fields = '__all__'

class ReservationExtensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationExtension
        fields = '__all__'

class ReservationModificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationModification
        fields = '__all__'

class ReservationSupportTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationSupportTicket
        fields = '__all__'

class ReservationOccupancySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationOccupancy
        fields = '__all__'

class RevenueReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevenueReport
        fields = '__all__'

class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = '__all__'

class UserNotificationPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotificationPreferences
        fields = '__all__'
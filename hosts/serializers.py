# hosts/serializers.py
from rest_framework import serializers
from .models import Host
from .models import HostAvailability
from .models import HostBooking
from .models import HostMessage
from .models import HostPromotion
from .models import HostStatistics
from .models import HostEarnings
from .models import HostReservationPolicy
from .models import HostNotification
from .models import HostSupport

class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = '__all__'

class HostAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = HostAvailability
        fields = '__all__'


class HostBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostBooking
        fields = '__all__'

class HostMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostMessage
        fields = '__all__'


class HostPromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostPromotion
        fields = '__all__'


class HostStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostStatistics
        fields = '__all__'


class HostEarningsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostEarnings
        fields = '__all__'

class HostReservationPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = HostReservationPolicy
        fields = '__all__'


class HostNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostNotification
        fields = '__all__'

class HostSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostSupport
        fields = '__all__'

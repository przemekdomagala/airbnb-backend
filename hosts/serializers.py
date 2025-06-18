from rest_framework import serializers
from .models import Host
from .models import HostAvailability

class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = '__all__'

class HostAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = HostAvailability
        fields = '__all__'



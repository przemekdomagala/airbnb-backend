from rest_framework import viewsets, filters
from .models import Host
from .models import HostAvailability
from .serializers import HostSerializer
from .serializers import HostAvailability
from .serializers import HostAvailabilitySerializer

class HostViewSet(viewsets.ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['location']

class HostAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = HostAvailability.objects.all()
    serializer_class = HostAvailabilitySerializer
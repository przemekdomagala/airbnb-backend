from rest_framework import viewsets
from .models import Location
from .models import MapMarker
from .models import POI
from .models import MapAnnotation
from .models import MapBookmark
from .serializers import MapAnnotationSerializer
from .serializers import POISerializer
from .serializers import MapMarkerSerializer
from .serializers import LocationSerializer
from .serializers import MapBookmarkSerializer

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class MapMarkerViewSet(viewsets.ModelViewSet):
    queryset = MapMarker.objects.all()
    serializer_class = MapMarkerSerializer

class POIViewSet(viewsets.ModelViewSet):
    queryset = POI.objects.all()
    serializer_class = POISerializer

class MapAnnotationViewSet(viewsets.ModelViewSet):
    queryset = MapAnnotation.objects.all()
    serializer_class = MapAnnotationSerializer

class MapBookmarkViewSet(viewsets.ModelViewSet):
    queryset = MapBookmark.objects.all()
    serializer_class = MapBookmarkSerializer
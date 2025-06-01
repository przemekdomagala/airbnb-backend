from rest_framework import viewsets
from .models import (
    Location,
    MapMarker,
    POI,
    MapAnnotation,
    MapBookmark,
    MapLegend,
    MapUpdate,
    MapDownload,
    UserInteraction,
    MapTooltip,
)
from .serializers import (
    LocationSerializer,
    MapMarkerSerializer,
    POISerializer,
    MapAnnotationSerializer,
    MapBookmarkSerializer,
    MapLegendSerializer,
    MapUpdateSerializer,
    MapDownloadSerializer,
    UserInteractionSerializer,
    MapTooltipSerializer,
)

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

class MapLegendViewSet(viewsets.ModelViewSet):
    queryset = MapLegend.objects.all()
    serializer_class = MapLegendSerializer

class MapUpdateViewSet(viewsets.ModelViewSet):
    queryset = MapUpdate.objects.all()
    serializer_class = MapUpdateSerializer

class MapDownloadViewSet(viewsets.ModelViewSet):
    queryset = MapDownload.objects.all()
    serializer_class = MapDownloadSerializer

class UserInteractionViewSet(viewsets.ModelViewSet):
    queryset = UserInteraction.objects.all()
    serializer_class = UserInteractionSerializer

class MapTooltipViewSet(viewsets.ModelViewSet):
    queryset = MapTooltip.objects.all()
    serializer_class = MapTooltipSerializer

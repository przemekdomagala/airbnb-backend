from rest_framework import serializers
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

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class MapMarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapMarker
        fields = '__all__'

class POISerializer(serializers.ModelSerializer):
    class Meta:
        model = POI
        fields = '__all__'

class MapAnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapAnnotation
        fields = '__all__'

class MapBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapBookmark
        fields = '__all__'

class MapLegendSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapLegend
        fields = '__all__'

class MapUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapUpdate
        fields = '__all__'

class MapDownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapDownload
        fields = '__all__'

class UserInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInteraction
        fields = '__all__'

class MapTooltipSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapTooltip
        fields = '__all__'

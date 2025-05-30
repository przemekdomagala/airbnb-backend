from rest_framework import serializers
from .models import Location
from .models import MapMarker
from .models import POI
from .models import MapAnnotation
from .models import MapBookmark

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
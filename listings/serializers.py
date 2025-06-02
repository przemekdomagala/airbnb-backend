from rest_framework import serializers
from .models import Listing


class ListingSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Listing
        fields = [
            "id",
            "title",
            "description",
            "price_per_night",
            "location",
            "latitude",
            "longitude",
            "image_url",
            "created_at",
            "owner",
            "owner_username",
        ]
        read_only_fields = ["owner"]
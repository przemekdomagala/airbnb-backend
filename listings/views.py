from .models import Listing
from rest_framework import viewsets
from .serializers import ListingSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied
from django.db import models


# API ViewSet for regular listings (non-hotels)
@method_decorator(csrf_exempt, name="dispatch")
class ListingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows listings (non-hotels) to be viewed or edited.
    """

    queryset = Listing.objects.all()  # Default queryset
    serializer_class = ListingSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Return only listings that are NOT hotels, with optional filtering.
        """
        # Get all listings with property_type='listing'
        queryset = Listing.objects.filter(property_type='listing')
        
        # Apply additional filters
        sort_by = self.request.query_params.get("sort")
        location = self.request.query_params.get("location")

        if sort_by == "price_asc":
            queryset = queryset.order_by("price_per_night")
        elif sort_by == "price_desc":
            queryset = queryset.order_by("-price_per_night")
        elif sort_by == "oldest":
            queryset = queryset.order_by("created_at")
        else:  # newest
            queryset = queryset.order_by("-created_at")

        if location:
            queryset = queryset.filter(location__icontains=location)

        return queryset

    def perform_create(self, serializer):
        # This will automatically set the owner when creating
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)
        else:
            raise PermissionDenied("Authentication required to create listings.")


# API ViewSet for hotels only
@method_decorator(csrf_exempt, name="dispatch")
class HotelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows hotels to be viewed or edited.
    """

    queryset = Listing.objects.all()  # Default queryset
    serializer_class = ListingSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Return only listings that ARE hotels, with optional filtering.
        """
        # Get all listings with property_type='hotel'
        queryset = Listing.objects.filter(property_type='hotel')
        
        # Apply additional filters
        sort_by = self.request.query_params.get("sort")
        location = self.request.query_params.get("location")

        if sort_by == "price_asc":
            queryset = queryset.order_by("price_per_night")
        elif sort_by == "price_desc":
            queryset = queryset.order_by("-price_per_night")
        elif sort_by == "oldest":
            queryset = queryset.order_by("created_at")
        else:  # newest
            queryset = queryset.order_by("-created_at")

        if location:
            queryset = queryset.filter(location__icontains=location)

        return queryset

    def perform_create(self, serializer):
        # This will automatically set the owner when creating
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)
        else:
            raise PermissionDenied("Authentication required to create hotels.")

from .models import Listing, Advertisement, AdvertisementCategory
from rest_framework import viewsets
from .serializers import ListingSerializer, AdvertisementSerializer, AdvertisementCategorySerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q


# API ViewSet
@method_decorator(csrf_exempt, name="dispatch")
class ListingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows listings to be viewed or edited.
    """

    queryset = Listing.objects.all().order_by("-created_at")
    serializer_class = ListingSerializer

    def perform_create(self, serializer):
        # This will automatically set the owner when creating
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Optionally restricts the returned listings by filtering against
        query parameters in the URL.
        """
        queryset = Listing.objects.all()
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


@method_decorator(csrf_exempt, name="dispatch")
class AdvertisementViewSet(viewsets.ModelViewSet):
    """
    API endpoint for the new Advertisement system (private listings and hotels).
    """

    queryset = Advertisement.objects.select_related("category", "user").prefetch_related(
        "images", "pricing"    ).order_by("-created_at")
    serializer_class = AdvertisementSerializer

    def perform_create(self, serializer):
        # Handle both authenticated and anonymous users
        user = self.request.user if self.request.user.is_authenticated else None
        advertisement = serializer.save(user=user)
        
        # For anonymous users, store draft ID in session
        if not user and advertisement.status == 'draft':
            if 'anonymous_drafts' not in self.request.session:
                self.request.session['anonymous_drafts'] = []
            self.request.session['anonymous_drafts'].append(advertisement.advertisement_id)
            self.request.session.modified = True

    def get_queryset(self):
        """
        Filter advertisements by type, category, location, etc.
        Include anonymous drafts from session if user is not authenticated.
        """
        queryset = Advertisement.objects.select_related("category", "user").prefetch_related(
            "images", "pricing"
        ).all()        # Handle user-specific filtering
        if not self.request.user.is_authenticated:
            # For anonymous users, include public active ads + their session-based drafts
            anonymous_drafts = self.request.session.get('anonymous_drafts', [])
            queryset = queryset.filter(
                Q(status='active') |  # Public active listings
                Q(advertisement_id__in=anonymous_drafts, status='draft', user__isnull=True)  # Their drafts
            )
        else:
            # For authenticated users, show public active ads + their own ads (any status)
            queryset = queryset.filter(
                Q(status='active', user__isnull=False) |  # Public active listings
                Q(user=self.request.user)  # Their own listings (any status)
            )

        # Filter by advertisement type
        ad_type = self.request.query_params.get("type")
        if ad_type in ["private", "hotel"]:
            queryset = queryset.filter(advertisement_type=ad_type)

        # Filter by category
        category = self.request.query_params.get("category")
        if category:
            queryset = queryset.filter(category__name__icontains=category)

        # Filter by location
        location = self.request.query_params.get("location")
        if location:
            queryset = queryset.filter(location__icontains=location)

        # Filter by status
        status = self.request.query_params.get("status")
        if status:
            queryset = queryset.filter(status=status)

        # Sorting
        sort_by = self.request.query_params.get("sort")
        if sort_by == "price_asc":
            # For mixed types, we'll sort by advertisement_id for now
            # In a real system, you'd need more complex sorting logic
            queryset = queryset.order_by("advertisement_id")
        elif sort_by == "price_desc":
            queryset = queryset.order_by("-advertisement_id")
        elif sort_by == "newest":
            queryset = queryset.order_by("-created_at")
        elif sort_by == "oldest":
            queryset = queryset.order_by("created_at")
        else:
            queryset = queryset.order_by("-created_at")

        return queryset

    @action(detail=False, methods=["get"])
    def private_listings(self, request):
        """Get only private rental listings"""
        private_ads = self.get_queryset().filter(advertisement_type="private")
        serializer = self.get_serializer(private_ads, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def hotels(self, request):
        """Get only hotel advertisements"""
        hotel_ads = self.get_queryset().filter(advertisement_type="hotel")
        serializer = self.get_serializer(hotel_ads, many=True)
        return Response(serializer.data)


@method_decorator(csrf_exempt, name="dispatch")
class AdvertisementCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for advertisement categories.
    """

    queryset = AdvertisementCategory.objects.all()
    serializer_class = AdvertisementCategorySerializer

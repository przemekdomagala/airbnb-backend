from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# Keep legacy listings endpoint for backwards compatibility
router.register(r'listings', views.ListingViewSet)
# New advertisement-based system
router.register(r'advertisements', views.AdvertisementViewSet)
router.register(r'categories', views.AdvertisementCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Custom endpoints are automatically available via DRF actions:
    # /api/advertisements/private_listings/
    # /api/advertisements/hotels/
]
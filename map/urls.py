from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    LocationViewSet,
    MapMarkerViewSet,
    POIViewSet,
    MapAnnotationViewSet,
    MapBookmarkViewSet,
    MapLegendViewSet,
    MapUpdateViewSet,
    MapDownloadViewSet,
    UserInteractionViewSet,
    MapTooltipViewSet,
)

router = DefaultRouter()
router.register(r'locations', LocationViewSet)
router.register(r'map-markers', MapMarkerViewSet)
router.register(r'pois', POIViewSet)
router.register(r'map-annotations', MapAnnotationViewSet)
router.register(r'map-bookmarks', MapBookmarkViewSet)
router.register(r'map-legends', MapLegendViewSet)
router.register(r'map-updates', MapUpdateViewSet)
router.register(r'map-downloads', MapDownloadViewSet)
router.register(r'user-interactions', UserInteractionViewSet)
router.register(r'map-tooltips', MapTooltipViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

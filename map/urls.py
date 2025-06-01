from rest_framework.routers import DefaultRouter
from .views import LocationViewSet
from .views import MapMarkerViewSet
from .views import POIViewSet
from .views import MapAnnotationViewSet
from .views import MapBookmarkViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'locations', LocationViewSet)
router.register(r'map-markers', MapMarkerViewSet)
router.register(r'pois', POIViewSet)
router.register(r'map-annotations', MapAnnotationViewSet)
router.register(r'map-bookmarks', MapBookmarkViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

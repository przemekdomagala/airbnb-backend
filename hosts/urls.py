# hosts/urls.py
from rest_framework.routers import DefaultRouter
from .views import HostViewSet
from .views import HostAvailabilityViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'hosts', HostViewSet)
router.register(r'host-availability', HostAvailabilityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

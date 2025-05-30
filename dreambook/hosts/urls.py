# hosts/urls.py
from rest_framework.routers import DefaultRouter
from .views import HostViewSet
from .views import HostAvailabilityViewSet
from .views import HostBookingViewSet
from .views import HostMessageViewSet
from .views import HostPromotionViewSet
from .views import HostStatisticsViewSet
from .views import HostEarningsViewSet 
from .views import HostReservationPolicyViewSet
from .views import HostNotificationViewSet
from .views import HostSupportViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'hosts', HostViewSet)
router.register(r'host-availability', HostAvailabilityViewSet)
router.register(r'host-bookings', HostBookingViewSet)
router.register(r'host-messages', HostMessageViewSet)
router.register(r'host-promotions', HostPromotionViewSet)
router.register(r'host-statistics', HostStatisticsViewSet)
router.register(r'host-earnings', HostEarningsViewSet)
router.register(r'host-reservation-policy', HostReservationPolicyViewSet)
router.register(r'host-notifications', HostNotificationViewSet)
router.register(r'host-support', HostSupportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

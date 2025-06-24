from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'listings', views.ListingViewSet, basename='listing')
router.register(r'hotels', views.HotelViewSet, basename='hotel')

urlpatterns = [
    path('', include(router.urls)),
]
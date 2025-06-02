
from django.urls import path
from .views import FilteredPropertyListAPIView

urlpatterns = [
    path('properties/', FilteredPropertyListAPIView.as_view(), name='filtered-properties'),
]

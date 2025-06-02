from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path("register", views.RegisterAPIView.as_view(), name="api_register"),
    path("login", views.CustomObtainAuthToken.as_view(), name="api_token"),
    path("profile", views.UserProfileView.as_view(), name="api_profile"),
]

from django.urls import path
from . import views

urlpatterns = [
    # Auth endpoints expected by frontend
    path("auth/register", views.RegisterAPIView.as_view(), name="auth_register"),
    path("auth/login", views.LoginAPIView.as_view(), name="auth_login"),
    path("auth/refresh", views.RefreshTokenAPIView.as_view(), name="auth_refresh"),
    path("auth/logout", views.logout_view, name="auth_logout"),
    path("auth/me", views.user_profile_view, name="auth_me"),
    
    # Legacy endpoints (for backward compatibility)
    path("register", views.RegisterAPIView.as_view(), name="api_register"),
    path("login", views.LoginAPIView.as_view(), name="api_token"),
    path("profile", views.UserProfileView.as_view(), name="api_profile"),
]

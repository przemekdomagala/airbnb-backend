from django.urls import path
from .views import (
    RoleCreateView,
    PermissionCreateView,
    AssignRoleToUserView,
    AssignPermissionToRoleView,
    CheckAccessView,
)
urlpatterns = [
    path('roles/', RoleCreateView.as_view(), name='role-create'),
    path('permissions/', PermissionCreateView.as_view(), name='permission-create'),
    path('assign-role-to-user/', AssignRoleToUserView.as_view(), name='assign-role-to-user'),
    path('assign-permission-to-role/', AssignPermissionToRoleView.as_view(), name='assign-permission-to-role'),
    path('check-access/', CheckAccessView.as_view(), name='check-access'),
]
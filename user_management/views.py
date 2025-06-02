from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Role, Permission, RolePermission, UserRole
from .serializers import RoleSerializer, PermissionSerializer, RolePermissionSerializer, UserRoleSerializer
from django.contrib.auth.models import User
from rest_framework import status

class RoleCreateView(generics.CreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class PermissionCreateView(generics.CreateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

class AssignRoleToUserView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        role_id = request.data.get('role_id')

        try:
            user = User.objects.get(id=user_id)
            role = Role.objects.get(id=role_id)

            user_role, created = UserRole.objects.get_or_create(user=user, role=role)

            return Response({'created': created}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Role.DoesNotExist:
            return Response({'error': 'Role not found'}, status=status.HTTP_404_NOT_FOUND)

class AssignPermissionToRoleView(APIView):
    def post(self, request):
        role_id = request.data.get('role_id')
        permission_id = request.data.get('permission_id')

        try:
            role = Role.objects.get(id=role_id)
            permission = Permission.objects.get(id=permission_id)
        except (Role.DoesNotExist, Permission.DoesNotExist):
            return Response({'error': 'Role or Permission not found.'}, status=status.HTTP_404_NOT_FOUND)

        role_permission, created = RolePermission.objects.get_or_create(role=role, permission=permission)

        return Response({'message': 'Permission assigned successfully.'})


class CheckAccessView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        permission_name = request.data.get('permission_name')

        try:
            user = User.objects.get(id=user_id)
            user_role = UserRole.objects.get(user=user)
        except (User.DoesNotExist, UserRole.DoesNotExist):
            return Response({'access': False, 'reason': 'No user or role assigned.'}, status=status.HTTP_404_NOT_FOUND)

        # Szukamy, czy rola ma przypisane to permission
        has_permission = RolePermission.objects.filter(
            role=user_role.role,
            permission__name=permission_name
        ).exists()

        return Response({'access': has_permission})

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)  # GUEST, CLIENT, HOST, ADMIN
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.role.name} -> {self.permission.name}"

class UserRole(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        # Keep any other field options you had previously
    )
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}: {self.role.name}"

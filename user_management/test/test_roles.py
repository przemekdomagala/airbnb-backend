import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from user_management.models import Role

@pytest.mark.django_db
def test_create_role():
    client = APIClient()
    response = client.post('/api/users/roles/', {
        'name': 'TESTER',
        'description': 'Tester systemu'
    })
    assert response.status_code == 201
    assert Role.objects.filter(name='TESTER').exists()

@pytest.mark.django_db
def test_assign_role_to_user():
    client = APIClient()
    user = User.objects.create(username='testuser')
    role = Role.objects.create(name='CLIENT')

    response = client.post('/api/users/assign-role-to-user/', {
        'user_id': user.id,
        'role_id': role.id
    })

    assert response.status_code == 201
    assert user.userrole.role == role

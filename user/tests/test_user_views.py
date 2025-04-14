import os
import django
import uuid

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Library_project.settings')
django.setup()

import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


# Helper functions to get URLs
def get_register_url():
    return reverse('user:create')


def get_login_url():
    return reverse('user:login')


def get_me_url():
    return reverse('user:manage')


# Test for CreateUserView
@pytest.mark.django_db
def test_create_user(client):
    payload = {"email": f"new_{uuid.uuid4()}@example.com", "password": "testpass123"}
    response = client.post(get_register_url(), payload, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert 'email' in response.data
    assert response.data['email'] == payload['email']
    assert 'password' not in response.data


# Test for LoginUserView (valid credentials)
@pytest.mark.django_db
def test_login_user_valid(client):
    email = f"auth_{uuid.uuid4()}@example.com"
    password = "testpass123"
    user = User.objects.create_user(email=email, password=password)

    login_data = {
        'email': email,
        'password': password
    }
    response = client.post(get_login_url(), login_data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert 'token' in response.data
    assert response.data['token']


# Test for LoginUserView (invalid credentials)
@pytest.mark.django_db
def test_login_user_invalid(client):
    login_data = {
        'email': 'wrong@example.com',
        'password': 'wrongpass'
    }
    response = client.post(get_login_url(), login_data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'token' not in response.data


# Test for ManageUserView (authenticated user)
@pytest.mark.django_db
def test_manage_user_authenticated(client):
    email = f"auth_{uuid.uuid4()}@example.com"
    password = "testpass123"
    user = User.objects.create_user(email=email, password=password)

    login_data = {
        'email': email,
        'password': password
    }
    login_response = client.post(get_login_url(), login_data, format='json')
    token = login_response.data['token']

    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.get(get_me_url(), format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['email'] == email


# Test for ManageUserView (unauthenticated user)
@pytest.mark.django_db
def test_manage_user_unauthenticated(client):
    response = client.get(get_me_url(), format='json')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


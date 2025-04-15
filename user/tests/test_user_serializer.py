import os
import uuid

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Library_project.settings')
django.setup()


import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from user.serializers import UserSerializer, AuthTokenSerializer


User = get_user_model()

@pytest.fixture
def client():
    return APIClient()

@pytest.mark.django_db
def test_user_serializer_create_user():
    payload = {"email": f"new_{uuid.uuid4()}@example.com", "password": "testpass123"}
    serializer = UserSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors
    user = serializer.save()

    assert user.email == payload["email"]
    assert user.check_password(payload["password"])


@pytest.mark.django_db
def test_user_serializer_password_write_only():
    email = f"test2_{uuid.uuid4()}@example.com"
    user = User.objects.create_user(email=email, password="testpass123")
    serializer = UserSerializer(user)

    assert "password" not in serializer.data


@pytest.mark.django_db
def test_auth_token_serializer_valid_credentials(client):
    email = f"auth_{uuid.uuid4()}@example.com"
    user = User.objects.create_user(email=email, password="testpass123")
    serializer = AuthTokenSerializer(data={
        "email": email,
        "password": "testpass123"
    }, context={"request": None})
    assert serializer.is_valid(), serializer.errors
    assert "token" in serializer.validated_data


@pytest.mark.django_db
def test_auth_token_serializer_invalid_credentials(client):
    email = f"authfail_{uuid.uuid4()}@example.com"
    User.objects.create_user(email=email, password="testpass123")
    serializer = AuthTokenSerializer(data={
        "email": email,
        "password": "wrongpass"
    }, context={"request": None})
    with pytest.raises(Exception):
        serializer.is_valid(raise_exception=True)

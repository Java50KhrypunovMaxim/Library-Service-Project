import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Library_project.settings')
django.setup()

import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_create_user_success():
    user = User.objects.create_user(
        email="test1@example.com",
        password="testpass123"
    )

    assert user.email == "test1@example.com"
    assert user.check_password("testpass123")
    assert not user.is_staff
    assert not user.is_superuser


@pytest.mark.django_db
def test_create_user_no_email_error():
    with pytest.raises(ValueError):
        User.objects.create_user(email=None, password="testpass123")

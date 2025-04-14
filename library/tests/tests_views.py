import os
import django
import uuid

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Library_project.settings')
django.setup()

import pytest
from rest_framework.test import APIClient
from rest_framework import status
from library.models import Book, User, Payment, Borrowing

import datetime

@pytest.fixture
def user():
    return User.objects.create_user(
        email=f"testuser_{uuid.uuid4().hex}@example.com",
        password="password123"
    )


@pytest.fixture
def admin_user():
    return User.objects.create_superuser(email="admin@example.com", password="admin123")


@pytest.fixture
def test_book():
    return Book.objects.create(
        title="Test Book",
        author="Test Author",
        cover=Book.CoverType.HARD,
        inventory=5,
        daily_fee=4.00
    )


@pytest.fixture
def test_borrowing(user, test_book):
    return Borrowing.objects.create(
        user=user,
        book=test_book,
        borrow_date=datetime.date(2025, 5, 1),
        expected_return_date=datetime.date(2025, 5, 10),
        actual_return_date=None
    )


@pytest.fixture
def test_payment(test_borrowing):
    return Payment.objects.create(
        borrowing=test_borrowing,
        session_url="https://fake-payment.com/session/12345",
        session_id="12345",
        money_to_pay=36.00
    )


@pytest.mark.django_db
class TestBookViewSet:
    def test_book_list(self, user, test_book):
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get("/api/library/books/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_book_detail(self, user, test_book):
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get(f"/api/library/books/{test_book.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == test_book.id
        assert response.data["title"] == "Test Book"

    def test_book_filter_by_title(self, user, test_book):
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get("/api/library/books/", {"title": "Test Book"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]["title"] == "Test Book"

    def test_book_filter_by_author(self, user, test_book):
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get("/api/library/books/", {"author": "Test Author"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]["author"] == "Test Author"


@pytest.mark.django_db
class TestPaymentViewSet:
    def test_payment_list(self, user, test_payment):
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get("/api/library/payments/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0


@pytest.mark.django_db
class TestBorrowingViewSet:
    def test_borrowing_list(self, user, test_borrowing):
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get("/api/library/borrowings/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_borrowing_detail(self, user, test_borrowing):
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get(f"/api/library/borrowings/{test_borrowing.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == test_borrowing.id
        assert response.data["borrow_date"] == "2025-05-01"
        assert response.data["expected_return_date"] == "2025-05-10"


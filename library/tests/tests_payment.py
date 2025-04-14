import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Library_project.settings')
django.setup()


import pytest
from django.contrib.auth import get_user_model
from library.models import Book, Borrowing, Payment
from datetime import date

User = get_user_model()

@pytest.fixture(autouse=True)
def clear_users():
    User.objects.all().delete()  # Удаление всех пользователей перед каждым тестом

@pytest.fixture
def user():
    return User.objects.create_user(
        email="testuser@example.com",
        password="password123"
    )

@pytest.fixture
def book():
    return Book.objects.create(
        title="Test Book",
        author="Test Author",
        cover=Book.CoverType.HARD,
        inventory=5,
        daily_fee=4.00
    )

@pytest.fixture
def borrowing(user, book):
    return Borrowing.objects.create(
        user=user,
        book=book,
        borrow_date=date(2025, 4, 13),
        expected_return_date=date(2025, 4, 18),
        actual_return_date=date(2025, 4, 14)
    )

@pytest.mark.django_db
def test_create_payment(borrowing):
    payment = Payment.objects.create(
        borrowing=borrowing,
        session_url="https://fake-payment.com/session/12345",
        session_id="12345",
        money_to_pay=20
    )

    assert payment.borrowing == borrowing
    assert payment.money_to_pay == 4
    assert payment.type == Payment.Type.PAYMENT
    assert payment.status == Payment.Status.PENDING

    assert payment.session_id == "12345"
    assert payment.session_url == "https://fake-payment.com/session/12345"

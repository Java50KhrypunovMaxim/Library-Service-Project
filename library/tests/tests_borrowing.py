import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Library_project.settings')
django.setup()

import pytest
from django.utils.crypto import get_random_string
from datetime import date, datetime
from library.models import Book, Borrowing
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        email=f"user{get_random_string(6)}@example.com",
        password="password123"
    )


@pytest.mark.django_db
def test_create_borrowing(user):
    book = Book.objects.create(
        title="Test Book",
        author="Test Author",
        cover=Book.CoverType.HARD,
        inventory=10,
        daily_fee=3.50
    )
    borrowing = Borrowing.objects.create(
        user=user,
        book=book,
        borrow_date=date(2025, 4, 1),
        expected_return_date=date(2025, 4, 10)
    )

    assert borrowing.user == user
    assert borrowing.book == book
    assert borrowing.borrow_date == date(2025, 4, 1)
    assert borrowing.expected_return_date == date(2025, 4, 10)
    assert str(borrowing) == f"Test Book borrowed by {user.email}"


@pytest.mark.django_db
def test_create_borrowing_with_actual_return(user):
    book = Book.objects.create(
        title="Returned Book",
        author="Author X",
        cover=Book.CoverType.SOFT,
        inventory=3,
        daily_fee=4.25
    )
    borrowing = Borrowing.objects.create(
        user=user,
        book=book,
        borrow_date=date(2025, 5, 1),
        expected_return_date=date(2025, 5, 10),
        actual_return_date=datetime.now().date()
    )

    assert borrowing.actual_return_date == datetime.now().date()
    assert borrowing.user == user
    assert borrowing.book == book
    assert str(borrowing) == f"Returned Book borrowed by {user.email}"


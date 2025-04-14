import os
import django
import pytest
import uuid
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Library_project.settings')
django.setup()

from library.models import Book, Payment, Borrowing, User
from library.serializers import (
    BookSerializer,
    PaymentSerializer,
    BorrowingSerializer,
    BookListSerializer,
    BorrowingListSerializer,
    PaymentListSerializer,
)

@pytest.fixture
def unique_user():
    return User.objects.create_user(
        email=f"testuser_{uuid.uuid4().hex}@example.com",
        password="password123"
    )

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
def test_borrowing(unique_user, test_book):
    borrow_date = datetime.date(2025, 5, 1)
    expected_return_date = datetime.date(2025, 5, 10)
    actual_return_date = datetime.date(2025, 5, 9)

    return Borrowing.objects.create(
        user=unique_user,
        book=test_book,
        borrow_date=borrow_date,
        expected_return_date=expected_return_date,
        actual_return_date=actual_return_date
    )

@pytest.mark.django_db
def test_book_serializer(test_book):
    serializer = BookSerializer(test_book)
    data = serializer.data

    assert data['id'] == test_book.id
    assert data['title'] == "Test Book"
    assert data['author'] == "Test Author"
    assert data['cover'] == "HARD"
    assert data['inventory'] == 5
    assert data['daily_fee'] == "4.00"

@pytest.mark.django_db
def test_book_list_serializer(test_book):
    serializer = BookListSerializer([test_book], many=True)
    data = serializer.data

    assert len(data) == 1
    assert data[0]['id'] == test_book.id
    assert data[0]['title'] == "Test Book"
    assert data[0]['author'] == "Test Author"

@pytest.mark.django_db
def test_payment_serializer(test_borrowing):
    payment = Payment.objects.create(
        borrowing=test_borrowing,
        session_url="https://fake-payment.com/session/12345",
        session_id="12345",
        money_to_pay=36.00
    )

    serializer = PaymentSerializer(payment)
    data = serializer.data

    assert data['id'] == payment.id
    assert data['status'] == "PENDING"
    assert data['type'] == "PAYMENT"
    assert data['borrowing'] == test_borrowing.id
    assert data['session_url'] == "https://fake-payment.com/session/12345"
    assert data['session_id'] == "12345"


@pytest.mark.django_db
def test_payment_list_serializer(test_borrowing):
    payment = Payment.objects.create(
        borrowing=test_borrowing,
        session_url="https://fake-payment.com/session/12345",
        session_id="12345",
        money_to_pay=36.00
    )

    serializer = PaymentListSerializer([payment], many=True)
    data = serializer.data

    assert len(data) == 1
    assert data[0]['session_url'] == "https://fake-payment.com/session/12345"
    assert data[0]['session_id'] == "12345"

@pytest.mark.django_db
def test_borrowing_serializer(test_borrowing):
    serializer = BorrowingSerializer(test_borrowing)
    data = serializer.data

    assert data['id'] == test_borrowing.id
    assert data['borrow_date'] == "2025-05-01"
    assert data['expected_return_date'] == "2025-05-10"
    assert data['actual_return_date'] == "2025-04-14"
    assert data['book'] == test_borrowing.book.id

@pytest.mark.django_db
def test_borrowing_list_serializer(test_borrowing):
    serializer = BorrowingListSerializer([test_borrowing], many=True)
    data = serializer.data

    assert len(data) == 1
    assert data[0]['book']['id'] == test_borrowing.book.id

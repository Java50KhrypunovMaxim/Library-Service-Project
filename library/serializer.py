from datetime import timezone
import stripe
from django.conf import settings

from rest_framework import serializers
from library.models import Book, Payment, Borrowing


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "cover", "inventory", "daily_fee")


class BookImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "cover_image")


class BookListSerializer(BookSerializer):
    author = serializers.StringRelatedField(read_only=True)


class BookDetailSerializer(BookSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Book
        fields = ("id", "title", "author", "description", "cover_image")


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("id", "status", "type", "borrowing", "session_url", "session_id", "money_to_pay")
        read_only_fields = ("money_to_pay", "session_url", "session_id")

    def create(self, validated_data):
        borrowing = validated_data["borrowing"]
        payment_type = validated_data["type"]

        if payment_type == Payment.Type.PAYMENT:
            money_to_pay = borrowing.book.daily_fee
        elif payment_type == Payment.Type.FINE:
            today = timezone.now().date()
            overdue_days = (today - borrowing.expected_return_date).days
            money_to_pay = overdue_days * borrowing.book.daily_fee if overdue_days > 0 else 0
        else:
            raise serializers.ValidationError("Invalid payment type")

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"{payment_type} for borrowing {borrowing.id}",
                    },
                    "unit_amount": int(money_to_pay * 100),  # Stripe принимает сумму в центах
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="https://yourdomain.com/success",
            cancel_url="https://yourdomain.com/cancel",
        )

        payment = Payment.objects.create(
            money_to_pay=money_to_pay,
            session_url=session.url,
            session_id=session.id,
            **validated_data
        )
        return payment



class PaymentListSerializer(PaymentSerializer):
    borrowing = serializers.StringRelatedField(read_only=True)


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "borrow_date", "expected_return_date", "actual_return_date", "book")

    def create(self, validated_data):
        return super().create(validated_data)


class BorrowingListSerializer(BorrowingSerializer):
    book = BookListSerializer(read_only=True)


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookDetailSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = ("id", "borrow_date", "expected_return_date", "actual_return_date", "book")

from rest_framework import serializers
from library.models import Book, Payment, Borrowing


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title",
                  "author", "cover",
                  "inventory", "daily_fee")


class BookListSerializer(BookSerializer):
    author = serializers.StringRelatedField(read_only=True)


class BookDetailSerializer(BookSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Book
        fields = ("id", "title",
                  "author", "cover",
                  "inventory", "daily_fee")


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("id", "status",
                  "type", "borrowing",
                  "session_url", "session_id",
                  "money_to_pay")
        read_only_fields = ("money_to_pay",
                            "session_url",
                            "session_id")


class PaymentListSerializer(PaymentSerializer):
    borrowing = serializers.StringRelatedField(read_only=True)


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "borrow_date",
                  "expected_return_date",
                  "actual_return_date", "book")

    def create(self, validated_data):
        return super().create(validated_data)


class BorrowingListSerializer(BorrowingSerializer):
    book = BookListSerializer(read_only=True)


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookDetailSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = ("id", "borrow_date",
                  "expected_return_date",
                  "actual_return_date", "book")

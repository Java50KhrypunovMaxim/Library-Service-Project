
from rest_framework import serializers
from library.models import Book, Payment, Borrowing


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "description", "cover_image")


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
        fields = ("id", "amount", "payment_date", "borrowing")


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

from rest_framework import mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from library.models import Book, Payment, Borrowing
from library.serializer import BookSerializer, BookListSerializer, BookDetailSerializer, PaymentSerializer, \
    PaymentListSerializer, BorrowingSerializer, BorrowingListSerializer


class BookViewSet(ReadOnlyModelViewSet,
                  mixins.CreateModelMixin,
                  GenericViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        if self.action == "retrieve":
            return BookDetailSerializer
        return BookSerializer

    def get_queryset(self):
        title = self.request.query_params.get("title")
        author = self.request.query_params.get("author")

        queryset = self.queryset

        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author__icontains=author)

        return queryset.distinct()

class PaymentPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

class PaymentViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     GenericViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    pagination_class = PaymentPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-created_at')

    def get_serializer_class(self):
        if self.action == "list":
            return PaymentListSerializer
        return PaymentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BorrowingViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       GenericViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    pagination_class = PaymentPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-borrow_date')

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        return BorrowingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

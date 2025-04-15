from django.urls import path, include
from rest_framework import routers

from library.views import BookViewSet, PaymentViewSet, BorrowingViewSet

router = routers.DefaultRouter()
router.register("books", BookViewSet)
router.register("payments", PaymentViewSet)
router.register("borrowings", BorrowingViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "library"

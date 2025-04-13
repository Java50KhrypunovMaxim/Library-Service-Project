from django.db import models

from user.models import User


class Book(models.Model):

    class CoverType(models.TextChoices):
        HARD = 'Hard Cover'
        SOFT = 'Soft Cover'

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=20, choices=CoverType.choices)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.title


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} borrowed {self.book.title}"


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING'
        PAID = 'PAID'

    class Type(models.TextChoices):
        PAYMENT = 'PAYMENT'
        FINE = 'FINE'

    status = models.CharField(max_length=7, choices=Status.choices, default=Status.PENDING)
    type = models.CharField(max_length=7, choices=Type.choices)
    borrowing = models.ForeignKey(Borrowing, on_delete=models.CASCADE)
    session_url = models.URLField(max_length=500)
    session_id = models.CharField(max_length=255)
    money_to_pay = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"{self.type} - {self.money_to_pay}$ ({self.status})"
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.crypto import get_random_string

User = get_user_model()


class Book(models.Model):

    class CoverType(models.TextChoices):
        HARD = 'HARD', 'Hard Cover'
        SOFT = 'SOFT', 'Soft Cover'

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=20, choices=CoverType.choices)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.title


class Borrowing(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="borrowings")
    book = models.ForeignKey(Book,
                             on_delete=models.CASCADE,
                             related_name="borrowings")
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.title} borrowed by {self.user.email}"


class Payment(models.Model):

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PAID = 'PAID', 'Paid'

    class Type(models.TextChoices):
        PAYMENT = 'PAYMENT', 'Payment'
        FINE = 'FINE', 'Fine'

    status = models.CharField(max_length=7,
                              choices=Status.choices,
                              default=Status.PENDING)
    type = models.CharField(max_length=7, choices=Type.choices)
    borrowing = models.ForeignKey(Borrowing,
                                  on_delete=models.CASCADE,
                                  related_name="payments")
    session_url = models.URLField(max_length=500)
    session_id = models.CharField(max_length=255)
    money_to_pay = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"{self.type} - {self.money_to_pay}$ ({self.status})"

    def save(self, *args, **kwargs):
        borrowing = self.borrowing
        borrow_date = borrowing.borrow_date
        return_date = (borrowing.actual_return_date
                       or borrowing.expected_return_date)
        days = (return_date - borrow_date).days
        if days == 0:
            days = 1
        daily_fee = borrowing.book.daily_fee
        self.money_to_pay = daily_fee * days

        if not self.session_id:
            self.session_id = get_random_string(length=32)
        if not self.session_url:
            self.session_url = \
                f"https://fake-payment.com/session/{self.session_id}"

        if borrowing.actual_return_date:
            if borrowing.actual_return_date > borrowing.expected_return_date:
                self.type = self.Type.FINE
            else:
                self.type = self.Type.PAYMENT
        else:
            self.type = self.Type.PAYMENT

        super().save(*args, **kwargs)

from django.contrib import admin

from library.models import Book, Borrowing, Payment

admin.site.register(Book)
admin.site.register(Borrowing)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    readonly_fields = ("money_to_pay",
                       "session_url",
                       "session_id")
    list_display = ("id",
                    "borrowing",
                    "money_to_pay",
                    "status",
                    "type",
                    "session_url",)

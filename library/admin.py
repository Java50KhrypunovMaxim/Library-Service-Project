from django.contrib import admin

from library.models import Book, Borrowing, Payment

admin.site.register(Book)
admin.site.register(Borrowing)
admin.site.register(Payment)


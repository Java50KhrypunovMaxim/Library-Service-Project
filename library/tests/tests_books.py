import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Library_project.settings')
django.setup()

import pytest
from library.models import Book, Borrowing


@pytest.mark.django_db
def test_create_book():
    book = Book.objects.create(
        title="Sample Book",
        author="Sample Author",
        cover=Book.CoverType.SOFT,
        inventory=15,
        daily_fee=4.99
    )

    assert book.title == "Sample Book"
    assert book.author == "Sample Author"
    assert book.cover == Book.CoverType.SOFT
    assert book.inventory == 15
    assert book.daily_fee == 4.99
    assert str(book) == "Sample Book"
from django.contrib import admin

from .models import Book, Author

# todo - add list of books inline for Author?

admin.site.register(Book)
admin.site.register(Author)

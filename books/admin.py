from django.contrib import admin

from .models import Book, Author


class BookAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_published'


class AuthorAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('first_name', 'last_name')


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from books.views import HomepageView, BookListView, BookDetailView, AuthorListView, AuthorDetailView, SearchResultsView


urlpatterns = [
    path('', HomepageView.as_view(), name='home'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('books/', BookListView.as_view(), name='books'),
    path('books/<uuid:pk>', BookDetailView.as_view(), name='book_detail'),
    path('authors/', AuthorListView.as_view(), name='authors'),
    path('authors/<int:pk>', AuthorDetailView.as_view(), name='author_detail'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
]

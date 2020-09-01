from django.urls import path
from django.views.generic import TemplateView

from books.views import BookListView, BookDetailView, AuthorListView, AuthorDetailView, SearchResultsView, \
    ReviewDeleteView, ReviewEditView

urlpatterns = [
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('books/', BookListView.as_view(), name='books'),
    path('books/<uuid:pk>', BookDetailView.as_view(), name='book_detail'),
    path('authors/', AuthorListView.as_view(), name='authors'),
    path('authors/<int:pk>', AuthorDetailView.as_view(), name='author_detail'),
    path('review/<int:pk>', ReviewDeleteView.as_view(), name='review_delete'),
    path('review/edit/<int:pk>', ReviewEditView.as_view(), name='review_edit'),
]

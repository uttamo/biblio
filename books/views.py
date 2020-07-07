import datetime as dt

from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q

from .models import Book, Author


class HomepageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['current_time'] = dt.datetime.now()
        return context_data


class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'


class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'


class AuthorListView(ListView):
    model = Author
    template_name = 'books/authors_list.html'
    context_object_name = 'authors'


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'books/author_detail.html'


class SearchResultsView(ListView):
    template_name = 'books/search_results.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        query = self.request.GET.get('query')
        context_data['query'] = query
        context_data['author_results'] = Author.objects.filter(
            Q(first_name__icontains=query) | Q(middle_name__icontains=query) | Q(last_name__icontains=query))
        return context_data

    def get_queryset(self):
        query = self.request.GET.get('query')
        qs = Book.objects.filter(Q(title__icontains=query) | Q(authors__first_name__icontains=query) | Q(
            authors__middle_name__icontains=query) | Q(authors__last_name__icontains=query)).distinct()
        return qs

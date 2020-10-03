from django.db.models import Q
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, FormView, DeleteView, UpdateView
from django.views.generic.detail import SingleObjectMixin

from .forms import ReviewForm
from .models import Book, Author, Review


class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()

        # Sorting of the list
        sorting_option = self.request.GET.get('sort')
        if sorting_option:
            sorting_param = {
                'title_asc': 'title',
                'title_desc': '-title',
                'author_asc': 'authors__full_name',
                'author_desc': '-authors__full_name',
            }.get(sorting_option)
            if sorting_param:
                queryset = queryset.order_by(sorting_param)
        return queryset


class BookDetailView(View):
    """
    For GET, dispatch to the display view.
    For POST, dispatch to the form POST view (form is in the detail page).
    """
    model = Book
    template_name = 'books/book_detail.html'

    def get(self, request, *args, **kwargs):
        view = _BookDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = _ReviewView.as_view()
        return view(request, *args, **kwargs)


class _BookDisplay(DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        all_reviews = book.reviews.all()
        user_review = None
        other_users_reviews = []
        for review in all_reviews:
            if review.user == self.request.user:
                assert user_review is None, f'There should only be one review per user per book: {review}'
                user_review = review
            else:
                other_users_reviews.append(review)
        context['other_reviews'] = other_users_reviews
        if user_review:
            context['existing_review'] = user_review
        else:
            context['form'] = ReviewForm()
        return context


class _ReviewView(SingleObjectMixin, FormView):
    template_name = 'books/book_detail.html'
    form_class = ReviewForm
    model = Book

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        new_review = form.save(commit=False)
        new_review.book = self.object
        new_review.user = self.request.user
        new_review.save()
        return super().form_valid(form)

    def get_success_url(self):
        """ After successful review submission, just go back to the book's page. """
        return reverse('book_detail', kwargs={'pk': self.object.pk})


class ReviewDeleteView(DeleteView):
    template_name = 'reviews/review_delete.html'
    model = Review

    def get_success_url(self):
        return reverse('book_detail', kwargs={'pk': self.object.book.pk})


class ReviewEditView(UpdateView):
    template_name = 'reviews/review_edit.html'
    model = Review
    fields = ['rating', 'text']

    def get_form_class(self):
        return ReviewForm

    def get_success_url(self):
        return reverse('book_detail', kwargs={'pk': self.object.book.pk})


class AuthorListView(ListView):
    model = Author
    template_name = 'books/authors_list.html'
    context_object_name = 'authors'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()

        # Sorting of the list
        sorting_option = self.request.GET.get('sort')
        if sorting_option:
            sorting_param = {
                'name_asc': ['first_name', 'middle_name', 'last_name'],
                'name_desc': ['-first_name', '-middle_name', '-last_name'],
            }.get(sorting_option)
            if sorting_param:
                queryset = queryset.order_by(*sorting_param)
        return queryset


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'books/author_detail.html'


class SearchResultsView(ListView):
    template_name = 'books/search_results.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        query = self.request.GET.get('query')
        context_data['query'] = query

        # Query on author name
        author_results = Author.objects.filter(
            Q(first_name__icontains=query) | Q(middle_name__icontains=query) | Q(last_name__icontains=query))
        # Add authors from the book results
        for book in self.get_queryset():
            author_results |= book.authors.all()
        context_data['author_results'] = set(author_results)
        return context_data

    def get_queryset(self):
        query = self.request.GET.get('query')
        qs = Book.objects.filter(Q(title__icontains=query) | Q(authors__first_name__icontains=query) | Q(
            authors__middle_name__icontains=query) | Q(authors__last_name__icontains=query)).distinct()
        return qs

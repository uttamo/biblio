from textwrap import shorten
from typing import Iterable
from uuid import uuid4

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
from django.db.models import UniqueConstraint
from django.urls import reverse_lazy


class Author(models.Model):
    first_name = models.CharField(max_length=128, blank=False)
    middle_name = models.CharField(max_length=128, blank=True)
    last_name = models.CharField(max_length=128, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f'<Author: "{self.full_name}">'

    @property
    def full_name(self):
        name = self.first_name
        if self.middle_name:
            name += f' {self.middle_name}'
        if self.last_name:
            name += f' {self.last_name}'
        return name

    def get_absolute_url(self):
        return reverse_lazy('author_detail', args=[str(self.pk)])


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author, related_name='books')
    description = models.TextField(max_length=500, blank=True)
    cover = models.ImageField(upload_to='book_covers/', blank=True)  # todo - maybe generate a filename with random chars
    date_published = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'<Book: "{self.title}">'

    @property
    def title_short(self) -> str:
        """ For list page. """
        return shorten(self.title, 70, placeholder="...")

    @property
    def author_str(self) -> str:
        return ', '.join(author.full_name for author in self.authors.all())

    def get_absolute_url(self) -> str:
        return reverse_lazy('book_detail', args=[str(self.pk)])

    def get_rating_info(self) -> dict:
        reviews: Iterable[Review] = self.review_set.all()
        no_of_reviews = len(reviews)
        total = sum(r.rating for r in reviews)

        if no_of_reviews == 0:
            average_rating = None
        else:
            average_rating = round(total / no_of_reviews, 1)

        info = {
            'no_of_reviews': no_of_reviews,
            'avg_rating': average_rating,
        }
        return info


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(blank=False, validators=[MinValueValidator(0), MaxValueValidator(10)])
    text = models.TextField(max_length=1000, blank=True, null=True)

    class Meta:
        constraints = [UniqueConstraint(fields=['user', 'book'], name='unique review per user per book')]

    def __str__(self):
        return f'<Review {self.pk} (by {self.user}) for {self.book} ({self.rating}/10)>'

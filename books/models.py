from uuid import uuid4

from django.db import models
from django.urls import reverse_lazy


class Author(models.Model):
    first_name = models.CharField(max_length=128, blank=False)
    middle_name = models.CharField(max_length=128, blank=True)
    last_name = models.CharField(max_length=128, blank=True)

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
    date_published = models.DateField(blank=True)

    def __str__(self):
        return f'<Book: "{self.title}">'

    @property
    def author_str(self):
        return ', '.join(author.full_name for author in self.authors.all())

    def get_absolute_url(self):
        return reverse_lazy('book_detail', args=[str(self.pk)])

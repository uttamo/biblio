from django.test import TestCase
from django.urls import reverse
from django.utils.html import escape

from .models import Book, Author


class BookTests(TestCase):
    def setUp(self):
        self.author1 = Author.objects.create(first_name='Walter',
                                             last_name='Isaacson')
        self.book1 = Book.objects.create(
            title='Steve Jobs',
            description='Biography of the Apple man',
            )
        self.book1.authors.add(self.author1)

    def test_book_object(self):
        self.assertEqual(self.book1.title, 'Steve Jobs')
        self.assertEqual(self.book1.title_short, 'Steve Jobs')
        self.assertEqual(self.book1.author_str, 'Walter Isaacson')

    def test_book_list_view(self):
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Steve Jobs')
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_book_detail_view(self):
        response = self.client.get(self.book1.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Steve Jobs')
        self.assertContains(response, 'Biography of the Apple man')
        self.assertTemplateUsed(response, 'books/book_detail.html')

        response_book_doesnt_exist = self.client.get('/books/12345/')
        self.assertEqual(response_book_doesnt_exist.status_code, 404)


class AuthorTests(TestCase):
    def setUp(self):
        # Author 1 (with a book)
        self.author1 = Author.objects.create(first_name='Walter',
                                             last_name='Isaacson')
        self.book1 = Book.objects.create(
            title='Steve Jobs',
            description='Biography of the Apple man',
        )
        self.book1.authors.add(self.author1)

        # Author 2
        self.author2 = Author.objects.create(first_name='Samuel',
                                             middle_name='Leroy',
                                             last_name='Jackson')

    def test_author_object(self):
        self.assertEqual(self.author1.full_name, 'Walter Isaacson')
        self.assertEqual(self.author2.full_name, 'Samuel Leroy Jackson')

    def test_author_list_view(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Walter Isaacson')
        self.assertContains(response, 'Samuel Leroy Jackson')
        self.assertTemplateUsed(response, 'books/author_list.html')

    def test_author_detail_view(self):
        response = self.client.get(self.author1.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Walter Isaacson')
        self.assertContains(response, 'Steve Jobs')  # book by author is listed on author's page
        self.assertTemplateUsed(response, 'books/author_detail.html')

        response_book_doesnt_exist = self.client.get('/authors/12345/')
        self.assertEqual(response_book_doesnt_exist.status_code, 404)


class SearchTests(TestCase):
    def setUp(self):
        # Author 1 (with two books)
        self.author1 = Author.objects.create(first_name='JK',
                                             last_name='Rowling')
        self.hp1 = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            description='The first book of the series',
        )
        self.hp1.authors.add(self.author1)
        self.hp2 = Book.objects.create(
            title="Harry Potter and the Chamber of Secrets",
            description='Second book with the big snake',
        )
        self.hp2.authors.add(self.author1)

        # Author 2 (with one books)
        self.author2 = Author.objects.create(first_name='Richard',
                                             last_name='Thaler')
        self.nudge = Book.objects.create(
            title='Nudge',
            description='The book draws on research in psychology and behavioural economics'
        )
        self.nudge.authors.add(self.author2)

    def test_1(self):
        response = self.client.get(reverse('search_results'), {'query': 'potter'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/search_results.html')

        # Stuff that should come up
        self.assertContains(response, 'Search results for "potter"')
        self.assertContains(response, 'JK Rowling')
        self.assertContains(response, "Harry Potter")
        self.assertContains(response, escape("Harry Potter and the Philosopher's Stone"))
        self.assertContains(response, "Harry Potter and the Chamber of Secrets")

        # Stuff that shouldn't come up
        self.assertNotContains(response, 'Richard Thaler')
        self.assertNotContains(response, 'Nudge')

    def test2(self):
        response = self.client.get(reverse('search_results'), {'query': 'STONE'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/search_results.html')

        # Stuff that should come up
        self.assertContains(response, 'Search results for "STONE"')
        self.assertContains(response, 'JK Rowling')
        self.assertContains(response, escape("Harry Potter and the Philosopher's Stone"))

        # Stuff that shouldn't come up
        self.assertNotContains(response, 'Richard Thaler')
        self.assertNotContains(response, "Harry Potter and the Chamber of Secrets")
        self.assertNotContains(response, 'Nudge')

    def test3(self):
        response = self.client.get(reverse('search_results'), {'query': 'nudge'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/search_results.html')

        # Stuff that should come up
        self.assertContains(response, 'Search results for "nudge"')
        self.assertContains(response, 'Richard Thaler')
        self.assertContains(response, 'Nudge')

        # Stuff that shouldn't come up
        self.assertNotContains(response, 'JK Rowling')
        self.assertNotContains(response, escape("Harry Potter and the Philosopher's Stone"))
        self.assertNotContains(response, "Harry Potter and the Chamber of Secrets")

# api/test_views.py
"""
Unit tests for Book API endpoints.

Covers:
- CRUD operations (create, retrieve, update, delete).
- Permissions: anonymous read-only; authenticated for create/update/delete.
- Validation: publication_year cannot be in the future.
- Filtering, searching, ordering on the list endpoint.

Run with:
    python manage.py test api
"""

from datetime import datetime, timedelta

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Author, Book

User = get_user_model()


class BookAPITests(APITestCase):
    def setUp(self):
        # Create two users: one regular user (authenticated) and one other for extra checks
        self.user = User.objects.create_user(username="tester", email="tester@example.com", password="password123")
        self.other_user = User.objects.create_user(username="other", email="other@example.com", password="password123")

        # Create authors
        self.author_1 = Author.objects.create(name="Author One")
        self.author_2 = Author.objects.create(name="Author Two")

        # Create books to use in list/search/filter tests
        self.book_a = Book.objects.create(title="Alpha Book", publication_year=2010, author=self.author_1)
        self.book_b = Book.objects.create(title="Beta Book", publication_year=2020, author=self.author_2)
        self.book_c = Book.objects.create(title="Gamma Python", publication_year=2015, author=self.author_1)

        # URLs (based on api/urls.py names used earlier)
        self.list_url = reverse("book-list")            # /api/books/
        self.create_url = reverse("book-create")        # /api/books/create/
        # detail/update/delete will be built per-instance with pk

    # ---------- Helper ----------
    def _detail_url(self, pk):
        return reverse("book-detail", args=[pk])

    def _update_url(self, pk):
        return reverse("book-update", args=[pk])

    def _delete_url(self, pk):
        return reverse("book-delete", args=[pk])

    # ---------- Permission & Read tests ----------
    def test_list_books_anonymous_allowed(self):
        """Anonymous users can GET the list of books (read-only)."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ensure returned count at least the ones we created
        returned_titles = [item["title"] for item in response.data]
        self.assertIn(self.book_a.title, returned_titles)
        self.assertIn(self.book_b.title, returned_titles)

    def test_retrieve_book_anonymous_allowed(self):
        """Anonymous user can retrieve detail of a book."""
        url = self._detail_url(self.book_a.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book_a.title)

    def test_create_book_requires_authentication(self):
        """POST requires authentication; anonymous should receive 401/403."""
        payload = {"title": "New Book", "publication_year": 2018, "author": self.author_1.pk}
        response = self.client.post(self.create_url, payload, format="json")
        # Depending on auth setup, could be 401 or 403; DRF typically returns 403 for unauthenticated in browsable API when using session auth.
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    # ---------- Authenticated CRUD tests ----------
    def test_create_book_authenticated(self):
        """Authenticated user can create a book and response contains saved data."""
        self.client.login(username="tester", password="password123")
        payload = {"title": "Created Book", "publication_year": 2019, "author": self.author_1.pk}
        response = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Created Book")
        # Confirm persisted
        self.assertTrue(Book.objects.filter(title="Created Book").exists())
        self.client.logout()

    def test_publication_year_validation_future_year(self):
        """Creating a book with publication_year in the future should be rejected by serializer validation."""
        self.client.force_login(self.user)
        next_year = datetime.now().year + 1
        payload = {"title": "Future Book", "publication_year": next_year, "author": self.author_1.pk}
        response = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Ensure validation error mentions publication_year
        self.assertIn("publication_year", response.data)

    def test_update_book_authenticated(self):
        """Authenticated user can update a book's title."""
        self.client.force_login(self.user)
        update_url = self._update_url(self.book_a.pk)
        payload = {"title": "Alpha Book Updated", "publication_year": self.book_a.publication_year, "author": self.author_1.pk}
        response = self.client.put(update_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Confirm update persisted
        self.book_a.refresh_from_db()
        self.assertEqual(self.book_a.title, "Alpha Book Updated")
        self.client.logout()

    def test_delete_book_authenticated(self):
        """Authenticated user can delete a book."""
        self.client.force_login(self.user)
        delete_url = self._delete_url(self.book_b.pk)
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book_b.pk).exists())
        self.client.logout()

    # ---------- Filtering / Search / Ordering ----------
    def test_filter_by_publication_year(self):
        """Filter list by exact publication_year via query param."""
        response = self.client.get(self.list_url, {"publication_year": 2020})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in response.data]
        self.assertEqual(titles, [self.book_b.title])  # only book_b matches 2020

    def test_filter_by_author(self):
        """Filter books by author id returns appropriate set."""
        response = self.client.get(self.list_url, {"author": self.author_1.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in response.data]
        # author_1 has book_a and book_c
        self.assertCountEqual(titles, [self.book_a.title, self.book_c.title])

    def test_search_by_title_or_author(self):
        """Search across title and author name using ?search= query."""
        # search by title fragment 'Python' should return book_c
        response = self.client.get(self.list_url, {"search": "Python"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in response.data]
        self.assertIn(self.book_c.title, titles)
        # search by author name 'Author Two' should return book_b
        response = self.client.get(self.list_url, {"search": "Author Two"})
        titles = [b["title"] for b in response.data]
        self.assertIn(self.book_b.title, titles)

    def test_ordering_by_publication_year_descending(self):
        """Ordering by -publication_year should return newest books first."""
        response = self.client.get(self.list_url, {"ordering": "-publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in response.data]
        # Confirm sorted descending
        self.assertEqual(years, sorted(years, reverse=True))

    # ---------- Permission enforcement checks ----------
    def test_anonymous_cannot_update_or_delete(self):
        """Ensure anonymous user cannot update or delete even if they try."""
        update_url = self._update_url(self.book_a.pk)
        response = self.client.put(update_url, {"title": "Hack", "publication_year": 2010, "author": self.author_1.pk}, format="json")
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        delete_url = self._delete_url(self.book_a.pk)
        response = self.client.delete(delete_url)
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_authenticated_user_other_actions(self):
        """
        Authenticated user should be able to perform actions.
        Also test partial updates (PATCH) if your UpdateView allows it.
        """
        self.client.force_login(self.user)
        patch_url = self._update_url(self.book_c.pk)
        response = self.client.patch(patch_url, {"title": "Patched Title"}, format="json")
        # Depending on UpdateView config, PATCH may be allowed; expect 200 on success
        if response.status_code == status.HTTP_200_OK:
            self.book_c.refresh_from_db()
            self.assertEqual(self.book_c.title, "Patched Title")
        else:
            # If PATCH is not allowed, ensure it fails with 405
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.client.logout()

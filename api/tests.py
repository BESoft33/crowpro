from django.test import TestCase
from unittest.mock import patch
from .auth import Staff
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from blog.models import Editorial, Article

User = get_user_model()


def mock_resolve_user(auth_header):
    if auth_header == "ValidToken":
        return "mock_user"
    return None


class StaffAuthenticationTest(TestCase):
    @patch('api.auth.resolve_user', side_effect=mock_resolve_user)
    def test_authenticate_valid_user(self, mock_resolve):
        request = type('Request', (object,), {"headers": {"Authorization": "ValidToken"}})()
        auth = Staff()
        user, _ = auth.authenticate(request)
        self.assertEqual(user, "mock_user")

    @patch('api.auth.resolve_user', side_effect=mock_resolve_user)
    def test_authenticate_invalid_user(self, mock_resolve):
        request = type('Request', (object,), {"headers": {"Authorization": "InvalidToken"}})()
        auth = Staff()
        result = auth.authenticate(request)
        self.assertIsNone(result)

    @patch('api.auth.resolve_user', side_effect=mock_resolve_user)
    def test_authenticate_no_auth_header(self, mock_resolve):
        request = type('Request', (object,), {"headers": {}})()
        auth = Staff()
        result = auth.authenticate(request)
        self.assertIsNone(result)


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.staff_user = User.objects.create_user(
            email='staff@example.com',
            password='password',
            is_staff=True,
            first_name='Staff',
            last_name='User'
        )
        self.regular_user = User.objects.create_user(
            email='user@example.com',
            password='password',
            first_name='Staff',
            last_name='User'
        )


class EditorialViewSetTests(AuthenticationTests):
    def setUp(self):
        super().setUp()
        self.editorial = Editorial.objects.create(
            title="Test Editorial",
            slug="test-editorial",
            content="Test content",
            created_by=self.staff_user
        )

    def test_list_editorials_unauthenticated(self):
        response = self.client.get('/editorials/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_editorial_as_staff(self):
        self.client.force_authenticate(user=self.staff_user)
        data = {
            "title": "New Editorial",
            "slug": "new-editorial",
            "content": "New content"
        }
        response = self.client.post('/editorials/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)

    def test_create_editorial_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post('/editorials/', {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_editorial(self):
        response = self.client.get(f'/editorials/{self.editorial.slug}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], self.editorial.slug)

    def test_update_editorial(self):
        self.client.force_authenticate(user=self.staff_user)
        data = {"title": "Updated Title"}
        response = self.client.patch(f'/editorials/{self.editorial.slug}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.editorial.refresh_from_db()
        self.assertEqual(self.editorial.title, "Updated Title")

    def test_delete_editorial(self):
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.delete(f'/editorials/{self.editorial.slug}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Editorial.objects.filter(slug=self.editorial.slug).exists())


class ArticleViewSetTests(AuthenticationTests):
    def setUp(self):
        super().setUp()
        self.author = User.objects.create_user(
            email='author@example.com',
            password='password',
            role=User.Role.AUTHOR,
            first_name='Author',
            last_name='User'
        )
        self.article = Article.objects.create(
            title="Test Article",
            slug="test-article",
            content="Test content",
            created_by=self.author
        )

    def test_list_articles_unauthenticated(self):
        response = self.client.get('/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_article_as_author(self):
        self.client.force_authenticate(user=self.author)
        data = {
            "title": "New Article",
            "content": "New content",
            "published": False
        }
        response = self.client.post('/articles/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['created_by']['email'], self.author.email)

    def test_publish_article_as_editor(self):
        editor = User.objects.create_user(
            email='editor@example.com',
            password='password',
            role=User.Role.EDITOR,
            first_name='Editor',
            last_name='User'
        )
        self.client.force_authenticate(user=editor)
        data = {"published": True}
        response = self.client.patch(f'/articles/{self.article.slug}/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_article(self):
        self.client.force_authenticate(user=self.author)
        response = self.client.delete(f'/articles/{self.article.slug}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(Article.objects.get(slug=self.article.slug).hide)


class UserViewSetTests(AuthenticationTests):
    def test_list_users_as_staff(self):
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get('/users/list_users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_update_user_profile(self):
        self.client.force_authenticate(user=self.regular_user)
        data = {"first_name": "Updated"}
        response = self.client.patch(f'/users/{self.regular_user.id}/manage/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.regular_user.refresh_from_db()
        self.assertEqual(self.regular_user.first_name, "Updated")

    def test_deactivate_user(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(f'/users/{self.regular_user.id}/manage/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.regular_user.refresh_from_db()
        self.assertFalse(self.regular_user.is_active)


class StatsViewTests(AuthenticationTests):
    def test_get_stats_as_staff(self):
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get('/stats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('article', response.data)
        self.assertIn('user_stats', response.data)

    def test_get_stats_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get('/stats/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostReadOnlyViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.author = User.objects.create_user(
            email='author@example.com',
            password='password',
            role=User.Role.AUTHOR,
            first_name='Author',
            last_name='User'
        )
        self.article = Article.objects.create(
            title="Public Article",
            slug="public-article",
            content="Content",
            published=True,
            created_by=self.author
        )

    def test_list_published_articles(self):
        response = self.client.get('api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_hidden_article(self):
        hidden_article = Article.objects.create(
            title="Hidden Article",
            slug="hidden-article",
            content="Content",
            hide=True,
            created_by=self.author
        )
        response = self.client.get(f'api/posts/{hidden_article.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

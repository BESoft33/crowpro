from django.test import TestCase

from .models import User


class AuthenticationTest(TestCase):
    def setUp(self):
        User.objects.create_user(email='test@email.com', password='testpass', first_name='Test', last_name='Test')
        User.objects.create_superuser(email='superuser@email.com', password='adminpass', first_name='Admin',
                                      last_name='Admin')

    def test_user_exists(self):
        user = User.objects.get(email='test@email.com')
        self.assertEqual(user, User.objects.get(email='test@email.com'))

    def test_user_is_admin(self):
        user = User.objects.get(email='superuser@email.com')
        self.assertTrue(user.is_superuser)

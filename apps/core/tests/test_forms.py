from django.test import TestCase
from django.contrib.auth.models import User
from apps.core.forms import LoginForm


class TestLoginForm(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpass123'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_loginform_valid_credentials(self):
        form = LoginForm(data={'username': self.username, 'password': self.password})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.user, self.user)

    def test_loginform_invalid_credentials(self):
        form = LoginForm(data={'username': self.username, 'password': 'wrongpass'})
        self.assertFalse(form.is_valid())
        self.assertIn('Incorrect username or password', form.errors['__all__'])
        # Ensure user is not set
        self.assertIsNone(getattr(form, 'user', None))

    def test_loginform_missing_username(self):
        form = LoginForm(data={'password': self.password})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_loginform_missing_password(self):
        form = LoginForm(data={'username': self.username})
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

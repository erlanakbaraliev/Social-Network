from django.contrib.auth.models import User
from django.urls import reverse

from apps.core.models import Post
from apps.core.utils_for_tests import BaseViewForTestCase


class TestLogin(BaseViewForTestCase):
    VIEW_NAME = 'login'

    def test_login_returns_200_http_response_uses_login_html(self):
        response = self.get_request()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/login.html')

    def test_post_login_correct_credentials(self):
        url = reverse(self.VIEW_NAME)
        data = {
            'username': self.user,
            'password': self.passwd
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        self.assertTrue(User.objects.filter(username=data['username']).exists())

    def test_post_login_incorrect_credentials(self):
        url = reverse(self.VIEW_NAME)
        data = {
            'username': 'incorrect',
            'password': 'incorrect'
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=data['username']).exists())


class TestRegister(BaseViewForTestCase):
    VIEW_NAME = 'register'

    def test_register_view_returns_200_http_response_uses_register_html(self):
        response = self.get_request()  # self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/register.html")

    def test_register_with_new_email_redirects(self):
        url = reverse(self.VIEW_NAME)
        data = {
            'username': 'aida',
            'email': 'aida@gmail.com',
            'password': 'aida',
            'password_confirmation': 'aida'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='aida').exists())
        self.assertRedirects(response, reverse("login"))

    def test_register_with_not_matching_passwords_raises_error(self):
        url = reverse(self.VIEW_NAME)
        data = {
            'username': 'aida',
            'email': 'aida@gmail.com',
            'password': 'aida',
            'password_confirmation': 'incorrect'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Passwords do not match")

    def test_pregister_existing_user_raises_error(self):
        url = reverse(self.VIEW_NAME)
        data = {
            'username': 'testuser',
            'email': 'testuser123@gmail.com',
            'password': '12345123',
            'password_confirmation': '12345123'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Username already exists")

    def test_register_existing_email_raises_error(self):
        url = reverse(self.VIEW_NAME)
        data = {
            'username': 'superuser',
            'email': 'admin@gmail.com',
            'password': '12345',
            'password_confirmation': '12345'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "An account with this email already exists.")


class TestIndex(BaseViewForTestCase):
    VIEW_NAME = 'index'

    def test_index_redirects_if_not_logged_in(self):
        response = self.get_request()
        self.assertRedirects(response, '/login?next=/')

    def test_index_logged_in_user(self):
        self.client.login(username='testuser', password='12345')
        response = self.get_request()

        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        self.client.login(username='testuser', password='12345')

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

        logout_url = reverse('logout')
        response = self.client.get(logout_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/')


class TestNewPost(BaseViewForTestCase):
    VIEW_NAME = 'new_post'

    def test_new_post_redirects_if_not_logged_in(self):
        response = self.get_request()
        self.assertRedirects(response, '/login?next=/new_post')

    def test_newpost_logged_in_user(self):
        self.client.login(username='testuser', password='12345')
        response = self.get_request()

        self.assertEqual(response.status_code, 200)

    def test_post_new_post(self):
        self.client.login(username='testuser', password='12345')
        url = reverse(self.VIEW_NAME)
        data = {
            'body': 'Some post'
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Post.objects.filter(body='Some post').exists())
        self.assertEqual(response.json()["message"], "Post successfully submitted!")

from django.urls import reverse
from django.contrib.auth.models import User

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
            'username': 'testuser',
            'password': '12345'
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
        self.assertEqual(response.context['message'], "Invalid username and/or password.")


class TestRegister(BaseViewForTestCase):
    VIEW_NAME = 'register'

    def test_register_view_returns_200_http_response_uses_register_html(self):
        response = self.get_request() # self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/register.html")

    def test_post_register_with_new_email(self):
        url = reverse(self.VIEW_NAME)
        data = {
            'username': 'aida',
            'email': 'aida@gmail.com',
            'password': 'aida',
            'confirmation': 'aida'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='aida').exists())
        self.assertRedirects(response, reverse("login"))

    # def test_post_register_with_existing_email(self):
    #     url = reverse(self.VIEW_NAME)
    #     data = {
    #         'username': 'erlan2',
    #         'email': 'erlan@msci.com',
    #         'password': 'erlan',
    #         'confirmation': 'erlan'
    #     }
    #     response = self.client.post(url, data)

    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response.content['message'], '')

    def test_post_register_with_not_matching_passwords(self):
        url = reverse(self.VIEW_NAME)
        data = {
            'username': 'aida',
            'email': 'aida@gmail.com',
            'password': 'aida',
            'confirmation': 'incorrect'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['message'], 'Passwords must match.')


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
            'new_post': 'Some post'
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Post.objects.filter(body='Some post').exists())

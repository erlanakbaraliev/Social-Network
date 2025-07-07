from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class BaseViewForTestCase(TestCase):
    VIEW_NAME = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.passwd = "12345"
        cls.user = User.objects.create_user(username='testuser', password=cls.passwd)
        cls.super_user = User.objects.create_superuser(username='superuser',
                                                       password=cls.passwd,
                                                       email="admin@gmail.com")

    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()

    def get_request(self, data=None, args=None, kwargs=None):
        if data:
            return self.client.get(reverse(self.VIEW_NAME, data))
        return self.client.get(reverse(self.VIEW_NAME, args=args, kwargs=kwargs))

    def post_request(self, data=None):
        return self.client.post(reverse(self.VIEW_NAME), data)

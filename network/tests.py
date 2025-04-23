from django.test import TestCase
# from .models import Post
from .models import Follow
from .models import User

class PostTest(TestCase):
    def setUp(self):
        aida = User.objects.create_user(username='aida',
                                        email='aida@gmail.com',
                                        password='123')
        aizi = User.objects.create_user(username='aizi',
                                        email='aizi@gmail.com',
                                        password='123')
        
        follow = Follow.objects.create(follower=aida, following=aizi)


    def test_follow(self):
        aida = User.objects.get(username='aida')
        aizi = User.objects.get(username='aizi')
        follow = Follow.objects.get(follower=aida, following=aizi)

        self.assertEqual(follow.follower, aida)
        self.assertEqual(follow.following, aizi)

    def test_follow_itself(self):
        aida = User.objects.get(username='aida')
        aizi = User.objects.get(username='aizi')
        follow = Follow.objects.get(follower=aida, following=aizi)

        self.assertEqual(follow.follower, aida)
        self.assertNotEqual(follow.following, aida)
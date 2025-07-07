from apps.core.utils_for_tests import BaseViewForTestCase
from apps.core.models import User, Post, Follow


class TestModels(BaseViewForTestCase):
    def test_follow_model(self):
        test_user = User.objects.get(username='testuser')
        super_user = User.objects.get(username='superuser')

        follow = Follow.objects.create(follower=test_user, following=super_user)

        self.assertEqual(str(follow), f'{follow.follower} follows {follow.following}')

    def test_post_model(self):
        user = User.objects.get(username='testuser')
        data = "Some data for post"

        post = Post.objects.create(user=user, body=data)

        self.assertEqual(str(post), f'{post.id} {post.user}: {post.body}')

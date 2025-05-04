from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(max_length=1000)
    time = models.DateTimeField(auto_now=True, auto_created=False)

    def __str__(self):
        return f"{self.time.date()} {self.user.username}: {self.content}"

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return f"{self.follower} follows {self.following}"

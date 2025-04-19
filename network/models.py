from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    title = models.CharField(max_length=120)
    body = models.TextField(max_length=1000)

    def __str__(self):
        return f"{self.title}: {self.body}"

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return f"{self.follower} follows {self.following}"
    
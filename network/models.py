from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=True)
    timedate = models.DateTimeField(auto_now_add=True)
    # likes = models.IntegerField()

    def __str__(self):
        return f"@{self.user} - {self.content} - {self.timedate.strftime('%Y-%m-%d- %H:%M')}"
    
class Follow(models.Model):
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed") 
    # Follow.objects.filter(followed=erlakba) => list of users/followers where erlakba is the followed
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    # Follow.objects.filter(follower=erlakba) => list of users/followed where erlakba is the follower

    def __str__(self):
        return f"{self.followed} is being followed by {self.follower}"
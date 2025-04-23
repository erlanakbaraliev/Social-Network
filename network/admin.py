from django.contrib import admin
from .models import Post
from .models import Follow
from .models import User


admin.site.register(User)
admin.site.register(Post)
admin.site.register(Follow)

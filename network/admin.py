from django.contrib import admin
from .models import Follow
from .models import User
from .models import Post

admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Post)

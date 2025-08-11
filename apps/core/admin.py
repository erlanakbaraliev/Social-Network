from django.contrib import admin

from apps.core.models import Follow, Post

admin.site.register(Post)
admin.site.register(Follow)

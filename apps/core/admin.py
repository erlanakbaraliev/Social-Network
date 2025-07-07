from django.contrib import admin

from apps.core.models import Post, Follow

admin.site.register(Post)
admin.site.register(Follow)

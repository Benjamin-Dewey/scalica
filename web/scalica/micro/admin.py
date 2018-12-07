from django.contrib import admin
from django.contrib.auth.models import User
from .models import Post, Following, ReverseFollowing

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Following)
admin.site.register(ReverseFollowing)

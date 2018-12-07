from django.contrib import admin
from .models import Post, Following, ReverseFollowing

# Register your models here.
admin.site.register(Post)
admin.site.register(Following)
admin.site.register(ReverseFollowing)

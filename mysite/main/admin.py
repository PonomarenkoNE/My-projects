from django.contrib import admin
from .models import Profile, Post, FolloweFollowing, LikeDislike

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(FolloweFollowing)
admin.site.register(LikeDislike)

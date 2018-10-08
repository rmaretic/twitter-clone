from django.contrib import admin
from .models import Posts, Follower

admin.site.register(Follower)
admin.site.register(Posts)

from django.contrib import admin
from .models import FriendRequest, Follow

admin.site.register(FriendRequest)
admin.site.register(Follow)
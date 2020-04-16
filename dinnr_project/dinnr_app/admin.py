from django.contrib import admin
from .models import UserProfile, FriendRequest, Session

admin.site.register(Session)
admin.site.register(UserProfile)
admin.site.register(FriendRequest)

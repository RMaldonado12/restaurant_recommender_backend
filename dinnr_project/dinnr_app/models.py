from django.db import models
from django.contrib.auth.models import User

from django.conf import settings

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_profile')
    username = models.CharField('username', max_length=250, null=True)
    first_name = models.CharField('First Name', max_length=250)
    last_name = models.CharField('Last Name', max_length=250)
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13)
    friends = models.ManyToManyField("UserProfile", blank=True)
    
    
class FriendRequest(models.Model):
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    timestamp = models.DateTimeField(auto_now_add=True) # timestamp for when request is created


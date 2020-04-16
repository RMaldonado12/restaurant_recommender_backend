from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractBaseUser

from django.conf import settings

from django.contrib.postgres.fields import ArrayField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user', primary_key=True,)
    phone_number = models.CharField(max_length=20, blank=True)
    friends = models.ManyToManyField("UserProfile", blank=True, related_name='UserProfile')
    
    
class FriendRequest(models.Model):
    ''' Set to_user to a ForeignKey to allow them to recieve multiple friend requests.  As a OneToOneField, they were not allowed to recieve more than one request. '''
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user', )
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    timestamp = models.DateTimeField(auto_now_add=True) # timestamp for when request is created
    accepted_status = models.BooleanField(default=False)

# class RestaurantSwipes(models.Model):
#     user_one_id = models.CharField(max_length=20)
#     user_two_id = models.CharField(max_length=20)
#     restaurant_list = ArrayField(ArrayField(
#             models.TextField()))
#     good_list = ArrayField(ArrayField(
#             models.TextField(blank=True)))
#     bad_list = ArrayField(ArrayField(
#            models.TextField(blank=True)))


class Session(models.Model):
    user_one = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_one')
    user_two = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_two')
    user_likes = ArrayField(models.CharField(max_length=50))
    zipcode = models.CharField(max_length=5)
    match = models.CharField(max_length=50)
    all_resteraunts = models.TextField()
    is_active = models.BooleanField(default=False)


'''
What if friends was it's own table?
    Get every Friend with the Users ID in to_user and from_user...
    If accepted == True, they are friends

..exactly what FriendRequest is.. duh!
----------------
Friends
    -to_user
    -from_user
    -accepted?
'''
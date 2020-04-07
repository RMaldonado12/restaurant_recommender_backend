from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings



class User(AbstractUser):
    username = models.CharField(blank=True, null=True, max_length=255)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

    def __str__(self):
        return "{}".format(self.email)

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profile')
    phone_number = models.CharField(max_length=13)
    email = models.CharField(max_length=100)
    friends = models.ManyToManyField("UserProfile", blank=True)
    first_name = models.CharField('First Name', max_length=250)
    last_name = models.CharField('Last Name', max_length=250)
    
    def __str__(self):
        return f'{self.user} profile..'
    
class FriendRequest(models.Model):
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='to_user')
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='from_user')
    timestamp = models.DateTimeField(auto_now_add=True) # timestamp for when request is created

    def __str__(self):
        return f'From {self.from_user.userName}, to {self.to_user.userName}'

from rest_framework import serializers
from dinnr_app.models import User, UserProfile, FriendRequest, Session
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from builtins import object

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','first_name','last_name')

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','first_name','last_name','password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = ('user', 'phone_number', 'friends')



class FriendRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendRequest
        fields = ('id', 'to_user', 'from_user', 'timestamp', 'accepted_status')


class UserDetailSerializer(object):
    def __init__(self, user):
        self.user = user

    @property
    def user_detail(self):
        return {
            'id': self.user.id,
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email
        }
    

class CustomFriendRequestSerializer(object):
    def __init__(self, friend_requests):
        self.friend_requests = friend_requests

    @property
    def all_requests(self):
        output = {'requests made': []}

        for f_request in self.friend_requests:
            details = {
                'from': f_request.from_user.id,
                'to': f_request.to_user.id,
                'accepted_status': f_request.accepted_status
            }
            output['requests made'].append(details)
        return output

class UserAccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ('id','username','email','first_name','last_name','password', 'phone_number', 'friends')


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('user_one', 'user_two', 'user_likes', 'all_resteraunts', 'zipcode', 'match', 'is_active')

    
from rest_framework import serializers
from dinnr_app.models import User, UserProfile, FriendRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


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
        fields = ('to_user', 'from_user', 'timestamp', 'accepted_status')


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
    

class UserAccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ('id','username','email','first_name','last_name','password', 'phone_number', 'friends')
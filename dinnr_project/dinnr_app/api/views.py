from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken

from dinnr_app.models import UserProfile, FriendRequest
from .serializers import UserSerializer, UserSignupSerializer, LoginSerializer, UserProfileSerializer, FriendRequestSerializer

class UserSignupView(generics.GenericAPIView):
    serializer_class = UserSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

class UserView(generics.RetrieveDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_object(self):
        return self.request.user

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permissions_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        return UserProfile.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FriendRequestView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        return FriendRequest.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    
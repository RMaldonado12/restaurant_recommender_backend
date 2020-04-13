from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken

from django.contrib.auth.models import User
from dinnr_app.models import UserProfile, FriendRequest
from .serializers import UserSerializer, UserSignupSerializer, LoginSerializer, UserProfileSerializer, FriendRequestSerializer, UserDetailSerializer, UserAccountSerializer


from django.http import JsonResponse



class UserSignupView(generics.GenericAPIView):
    serializer_class = UserSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        UserProfile.objects.create(user=user)
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


class UserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    serializer_class = UserSerializer
    
    def get_queryset(self):
        return User.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permissions_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        return UserProfile.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class UserFriendRequests(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permissions_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        """
            Return a list of all User FriendRequests
        """
        user = self.kwargs['user_pk']
        return FriendRequest.objects.filter(to_user=user)
    


class FriendRequestView(generics.ListCreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        return FriendRequest.objects.all()
    

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.multiple_lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


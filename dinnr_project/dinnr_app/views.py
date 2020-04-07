from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from dinnr_app.models import User, UserProfile, FriendRequest
from dinnr_app.serializers import UserSerializer, UserProfileSerializer, FriendRequestSerializer
from dinnr_app.permissions import IsLoggedInUserOrAdmin, IsAdminUser


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

class FriendRequestViewSet(viewsets.ModelViewSet):
    serializer_class = FriendRequestSerializer
    queryset = FriendRequest.objects.all()
    
# from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
# from django.contrib.auth.models import User

# from rest_framework import permissions, status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from .serializers import UserSerializer, UserSerializerWithToken

# @api_view(['GET'])
# def current_user(request):
#     serializer = UserSerializer(request.user)
#     return Response(serializer.data)

# class UserList(APIView):
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request, format=None):
#         serializer = UserSerializerWithToken(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from dinnr_app.models import User
from dinnr_app.serializers import UserSerializer
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
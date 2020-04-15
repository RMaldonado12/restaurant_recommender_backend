from rest_framework import viewsets, generics, permissions, mixins
from rest_framework.response import Response
from knox.models import AuthToken

from django.contrib.auth.models import User
from dinnr_app.models import UserProfile, FriendRequest
from .serializers import UserSerializer, UserSignupSerializer, LoginSerializer, UserProfileSerializer, FriendRequestSerializer, UserDetailSerializer, UserAccountSerializer, CustomFriendRequestSerializer


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


class UserCreateFriendRequest(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = FriendRequestSerializer

    def post(self, request):
        return self.create(request)






class FriendRequestView(generics.GenericAPIView,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin):
    '''
    
    '''
    serializer_class = FriendRequestSerializer
    queryset = FriendRequest.objects.all()
    #lookup_field = 'to_user'

    def get(self, request, user_pk=None):
        if user_pk:
            queryset = FriendRequest.objects.filter(to_user=user_pk)
            self.queryset = queryset
            return self.list(request)
        else:
            return self.list(request)

    def post(self, request, user_pk=None):
        to_user = request.data['to_user']
        from_user = request.data['from_user']
        
        if (FriendRequest.objects.filter(to_user=to_user, from_user=from_user).count() == 0):
            if (FriendRequest.objects.filter(to_user=from_user, from_user=to_user).count() == 0):
                return self.create(request)
        if (request.data['accepted_status'] == 'true'):
            # shhhhhh
            import pdb; pdb.set_trace()
            to_user, from_user = from_user, to_user
            the_object = FriendRequest.objects.filter(to_user=to_user, from_user=from_user)[0]
            FriendRequest.objects.get(id=the_object.id).delete()
            FriendRequest.objects.create(to_user=User.objects.get(id=to_user), from_user=User.objects.get(id=from_user), accepted_status=True)
            FriendRequest.objects.create(to_user=User.objects.get(id=from_user), from_user=User.objects.get(id=to_user), accepted_status=True)
            the_object = FriendRequest.objects.filter(to_user=to_user, from_user=from_user)
            to_user = User.objects.get(id=to_user)
            from_user = User.objects.get(id=from_user)
            to_user_profile = UserProfile.objects.get(user=to_user)
            from_user_profile = UserProfile.objects.get(user=from_user)
            #
            new_one = to_user_profile.friends.add(from_user_profile)
            new_two = from_user_profile.friends.add(to_user_profile)
            print('accepting...')
            
        if user_pk:
            queryset = FriendRequest.objects.filter(to_user=user_pk)
        else:
            queryset = FriendRequest.objects.all()
        self.queryset = queryset
        return self.list(request)
        

    def put(self, request, user_pk=None, from_user=None):
        return self.update(request, user_pk, to_user_pk)
    

# NOT USING ATM
#
#
# class FriendRequestView(generics.ListCreateAPIView):
#     serializer_class = FriendRequestSerializer
#     permission_classes = [
#         permissions.AllowAny
#     ]

#     def get_queryset(self):
#         return FriendRequest.objects.all()
    

#     def get_object(self):
#         queryset = self.get_queryset()
#         filter = {}
#         for field in self.multiple_lookup_fields:
#             filter[field] = self.kwargs[field]

#         obj = get_object_or_404(queryset, **filter)
#         self.check_object_permissions(self.request, obj)
#         return obj


def makeFriendRequest(request, from_user_pk, to_user_pk):
    print('test')
    print(from_user_pk)
    print(to_user_pk)

    from_user = User.objects.get(id=from_user_pk)
    to_user = User.objects.get(id=to_user_pk)

    ### NEED TO DO
    # Filter by from_user then filter by to_user before creating
    try:
        FriendRequest.objects.create(to_user=to_user, from_user=from_user)
        # serialize friend requests
        requests_made = FriendRequest.objects.filter(from_user=from_user.id)
        serialized = CustomFriendRequestSerializer(requests_made).all_requests
        return JsonResponse(data = serialized, status=200)
    except:
        print('Already a request in database')
        requests_made = FriendRequest.objects.filter(from_user=from_user.id)
        serialized = CustomFriendRequestSerializer(requests_made).all_requests
        import pdb;pdb.set_trace()
        return JsonResponse(data = serialized, status=200)

class HandleFriendRequests(generics.RetrieveUpdateDestroyAPIView):
    ## The from_user_pk and to_user_pk are from the url..
    def __init__(self, from_user_pk, to_user_pk):
        self.friend_request = FriendRequests.objects.filter(to_user=to_user_pk, from_user=from_user_pk)

    
    



class ProfilesView(generics.ListAPIView):
    serializer_class = UserSerializer
    permissions_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        return User.objects.all()

    def perform_create(self, serializer):
        serializer.save()
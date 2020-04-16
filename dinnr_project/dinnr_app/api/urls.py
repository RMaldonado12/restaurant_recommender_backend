from django.urls import path, include
from rest_framework import routers
from .views import UserSignupView, LoginView, UserView, UserProfileView, FriendRequestView, ProfilesView, UserCreateFriendRequest, SessionView
from . import views
from knox import views as knox_views


router = routers.DefaultRouter()
# router.register('api/users', UserView, 'users')
# router.register('api/auth/signup', UserSignupView, 'signup')
# router.register('api/auth/login', LoginView, 'login')

urlpatterns = [
    path('api/auth/signup/', UserSignupView.as_view(), name='signup'),
    path('api/auth/login/', LoginView.as_view(), name='login'),


    path('api/auth/user/', UserView.as_view(), name='user'),
    path('api/auth/user/<pk>/', UserView.as_view(), name='get_user_detail'),


    path('api/auth/profiles/', ProfilesView.as_view(), name='profile_list'),
    path('api/auth/profile/<pk>/', UserProfileView.as_view(), name='profile'),


    path('api/auth/friends/', FriendRequestView.as_view()),
    path('api/auth/friends/<int:user_pk>/', FriendRequestView.as_view()),
    # path('api/auth/friends/<int:user_pk>/', UserFriendRequests.as_view(), name='friendrequests'),

    path('api/auth/session/', SessionView.as_view(), name='session'),
    path('api/auth/session/<int:user_pk>/', SessionView.as_view(), name='session'),
    # path('api/auth/restList/<int:user_pk>/', views.start_new_session, name='new_session'),

 
    path('api/auth', include('knox.urls')),
    path('api/auth/logout', knox_views.LogoutView.as_view(), name='logout')
    # path('', include(router.urls)),
]
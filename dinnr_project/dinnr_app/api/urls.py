from django.urls import path, include
from rest_framework import routers
from .views import UserSignupView, LoginView, UserView, UserProfileView, FriendRequestView
from knox import views as knox_views


router = routers.DefaultRouter()
# router.register('api/users', UserView, 'users')
# router.register('api/auth/signup', UserSignupView, 'signup')
# router.register('api/auth/login', LoginView, 'login')

urlpatterns = [
    path('api/auth/signup/', UserSignupView.as_view(), name='signup'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/user/', UserView.as_view(), name='user'),
    path('api/auth/profile/<pk>/', UserProfileView.as_view(), name='profile'),
    path('api/auth/friends/<pk>/', FriendRequestView.as_view(), name='friends'),
    path('api/auth', include('knox.urls')),
    path('api/auth/logout', knox_views.LogoutView.as_view(), name='logout')
    # path('', include(router.urls)),
]
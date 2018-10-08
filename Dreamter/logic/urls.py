from django.urls import path
from . import views
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns


router = DefaultRouter()
router.register(r'', views.UserViewSet)


urlpatterns = [
    path('', views.api_root),
    path('users/', include(router.urls), name='users'),
    path('auth/', include('rest_framework.urls')),
    path('register/', views.Registration.as_view(), name='register_user'),
    path('private_timeline/', views.PrivateTimeline.as_view(), name='private_timeline'),
    path('public_timeline/', views.PublicTimeline.as_view(), name='public_timeline'),
    path('new/', views.NewPost.as_view(), name='new_post'),
    path('follow/', views.ToFollow.as_view(), name='follow'),
    path('ifollow/', views.UsersIFollow.as_view(), name='ifollow'),
    path('ifollow/<slug:username>/', views.UnfollowUser.as_view(), name='unfollow'),
]

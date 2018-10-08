from logic.models import User, Posts, Follower
from logic.serializers import UserSerializer, PostsSerializer, FollowerSerializer, CreateUserSerializer, DeleteFollowerSerializer
from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import detail_route, api_view
from rest_framework.views import APIView

@api_view(['GET'])
def api_root(request):
    return Response({
        'users': reverse('user-list', request=request),
        'public timeline': reverse('public_timeline', request=request),
        'private timeline': reverse('private_timeline', request=request),
        'register': reverse('register_user', request=request),
        'new post': reverse('new_post', request=request),
        'users to follow': reverse('follow', request=request),
        'users i follow': reverse('ifollow', request=request),
    })


class Registration(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"

    #shows all posts by username requested in url <slug:username>/posts
    @detail_route()
    def posts(self, request, username=None):
        user = self.get_object()
        posts = Posts.objects.filter(author=user).order_by('-datetime')
        posts_json = PostsSerializer(posts, many=True)
        return Response(posts_json.data)


class NewPost(generics.CreateAPIView):
    serializer_class = PostsSerializer
    permission_classes = [permissions.IsAuthenticated]


class PublicTimeline(generics.ListAPIView):
    queryset = Posts.objects.all().order_by('-datetime')
    serializer_class = PostsSerializer


class ToFollow(generics.ListCreateAPIView):
    """
    Shows list of users that authenticated user doesn't follow
    and allows user to follow users from that list by using POST
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        whoifollow = Follower.objects.filter(base_user=self.request.user)
        user_ids = [f.followed.id for f in whoifollow]
        user_list = User.objects.exclude(id__in=user_ids)
        return user_list

    #shows list of users if method is get
    #and allows to follow user if method is post
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        if self.request.method == 'POST':
            return FollowerSerializer

class UsersIFollow(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        whoifollow = Follower.objects.filter(base_user=self.request.user)
        user_ids = [f.followed.id for f in whoifollow]
        user_list = User.objects.filter(id__in=user_ids)
        return user_list

class UnfollowUser(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def delete(self, request, username):
        followed = User.objects.get(username=username)
        obj = Follower.objects.filter(base_user=self.request.user, followed=followed)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PrivateTimeline(generics.ListAPIView):
    serializer_class = PostsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        follower = Follower.objects.filter(base_user=self.request.user)
        user_ids = [f.followed.id for f in follower]
        posts = Posts.objects.filter(author__id__in=user_ids).order_by("datetime")
        return posts

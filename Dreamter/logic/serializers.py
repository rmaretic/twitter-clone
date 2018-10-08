from rest_framework import serializers
from logic.models import Posts, Follower
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class CreateUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'password')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ('author', 'post', 'datetime')

    def validate(self, data):
        if data["author"] != self.context['request'].user:
            raise serializers.ValidationError("You don't have permission to do that.")
        return data

class UserForeignKey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return User.objects.filter(username=self.context['request'].user)

class UsersToFollowForeignKey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        whoifollow = Follower.objects.filter(base_user=self.context['request'].user)
        user_ids = [f.followed.id for f in whoifollow]
        user_list = User.objects.exclude(id__in=user_ids)
        return user_list

class FollowerSerializer(serializers.ModelSerializer):
    base_user = UserForeignKey()
    followed = UsersToFollowForeignKey()
    class Meta:
        model = Follower
        fields = ('base_user', 'followed')

class DeleteFollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ('base_user', 'followed')
        lookup_field = 'followed'

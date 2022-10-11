from rest_framework import serializers
from django.contrib.auth.models import User
from postapi.models import UserProfile,Posts,Comments

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=[
            "username",
            "password",
            "email"
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserProfileSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    followings=UserSerializer(read_only=True,many=True)
    followers_count=serializers.CharField(read_only=True)
    class Meta:
        model=UserProfile
        fields="__all__"  # meansfollowings ozhike ellam venam

    def create(self, validated_data):
        user=self.context.get("user")
        return UserProfile.objects.create(user=user,**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    post=serializers.CharField(read_only=True)
    class Meta:
        model=Comments
        exclude=("date",) # means date ozhike ellam venam

    def create(self, validated_data):
        post=self.context.get("post")
        user=self.context.get("user")
        return Comments.objects.create(user=user,
                                       post=post,
                                       **validated_data)

class PostSerializer(serializers.ModelSerializer):
    author=serializers.CharField(read_only=True)
    fetch_comments=CommentSerializer(read_only=True,many=True)
    liked_by=UserSerializer(read_only=True,many=True)
    like_count=serializers.CharField(read_only=True)
    class Meta:
        model=Posts
        fields="__all__"


from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from postapi.serializers import UserSerializer,UserProfileSerializer,PostSerializer,CommentSerializer
from django.contrib.auth.models import User
from postapi.models import UserProfile,Posts
from rest_framework import permissions
from rest_framework.decorators import action

class UserRegistrationView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserProfileView(ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer=UserProfileSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    # localhost:8000/api/v1/users/profile/{pid}/follow
    @action(methods=["post"],detail=True)
    def follow(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        user_to_follow=User.objects.get(id=id)
        profile=UserProfile.objects.get(user=request.user)
        profile.followings.add(user_to_follow)
        return Response({"msg":"ok"})
    # localhost:8000/api/v1/users/profile/my_followings
    @action(methods=["get"],detail=False)
    def my_followings(self,request,*args,**kwargs):
        user=request.user
        user_profile=UserProfile.objects.get(user=user)
        followings=user_profile.followings.all()
        serializer=UserSerializer(followings,many=True)
        return Response(data=serializer.data)





class PostView(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Posts.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    #localhost:8000/api/v1/posts/{pid}/add_comment
    @action(methods=["post"],detail=True)
    def add_comment(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post=Posts.objects.get(id=id)
        user=request.user
        serializer=CommentSerializer(data=request.data,
                                     context={"post":post,
                                              "user":user
                                              })
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    # localhost:8000/api/v1/posts/{pid}/get_comments
    @action(methods=["get"],detail=True)
    def get_comments(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post=Posts.objects.get(id=id)
        comment=post.comments_set.all()
        serializer=CommentSerializer(comment,many=True)
        return Response(data=serializer.data)

    # localhost:8000/api/v1/posts/{pid}/add_like
    @action(methods=["post"], detail=True)
    def add_like(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post=Posts.objects.get(id=id)
        post.liked_by.add(request.user)
        return Response({"message":"liked"})

from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from .mixins import *

# Create your views here.


class PostImageViewSet(ModelViewSet):
    serializer_class = PostImageSerializer
    queryset = PostImage.objects.all()


class LikeViewSet(ModelViewSet):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class PostViewSet(ModelViewSet, PostDeleteMixin):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class GetPostViewSet(ModelViewSet):
    serializer_class = GetPostSerializer
    queryset = Post.objects.all()

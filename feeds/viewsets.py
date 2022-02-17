from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from .mixins import *


# Create your views here.
class PostImageViewSet(ModelViewSet):
    """ View sets for Post Images """

    serializer_class = PostImageSerializer
    queryset = PostImage.objects.all()


class LikeViewSet(ModelViewSet):
    """ View sets for Post Likes """

    serializer_class = LikeSerializer
    queryset = Like.objects.all()


class CommentViewSet(ModelViewSet):
    """ View sets for Post Comments """

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class PostViewSet(ModelViewSet, PostDeleteMixin):
    """ View sets for Posts """

    serializer_class = PostSerializer
    queryset = Post.objects.all()

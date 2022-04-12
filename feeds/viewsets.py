from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from .mixins import *


# Create your views here.
class PostViewSet(ModelViewSet, CreatePostMixin, HomeFeedPostsListMixin, PostDeleteMixin):
    """ View sets for Posts """

    serializer_class = PostSerializer
    queryset = Post.objects.all()

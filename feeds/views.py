from rest_framework.generics import GenericAPIView

from feeds.mixins import HomeFeedPostsListMixin
from feeds.models import Post
from feeds.serializers import GetPostSerializer


class GetPostViewSet(GenericAPIView, HomeFeedPostsListMixin):
    """ View to get Feed Posts of followed users in Homepage """

    serializer_class = GetPostSerializer
    queryset = Post.objects.all()

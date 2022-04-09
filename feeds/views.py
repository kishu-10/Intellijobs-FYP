from rest_framework.generics import GenericAPIView, ListAPIView
from feeds.mixins import HomeFeedPostsListMixin
from feeds.models import Post
from feeds.serializers import GetNetworkSerializer, GetPostSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class GetPostViewSet(GenericAPIView, HomeFeedPostsListMixin):
    """ View to get Feed Posts of followed users in Homepage """

    serializer_class = GetPostSerializer
    queryset = Post.objects.all()


class GetNetworksView(ListAPIView):
    """ View to get List of Organizations for network page """

    serializer_class = GetNetworkSerializer

    def get_queryset(self):
        return User.objects.filter(is_email_verified=True).exclude(user_type="Staff").exclude(pk=self.request.user.id).order_by('id')

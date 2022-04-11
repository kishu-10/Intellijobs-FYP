from rest_framework.generics import GenericAPIView, ListAPIView
from feeds.mixins import HomeFeedPostsListMixin
from feeds.models import Follower, Post
from feeds.serializers import FollowerSerializer, GetNetworkSerializer, GetPostSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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


class CreateNetworkView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FollowerSerializer(data=request.data)
        custom_data = {}
        if serializer.is_valid():
            if Follower.objects.filter(follower=self.request.user, being_followed=serializer.validated_data.get('being_followed')).exists():
                follower = Follower.objects.get(
                    follower=self.request.user, being_followed=serializer.validated_data.get('being_followed'))
                follower.is_active = not follower.is_active
                follower.save()
                if follower.is_active:
                    custom_data['message'] = "Followed"
                else:
                    custom_data['message'] = "Unfollowed"
            else:
                serializer.save(follower=self.request.user)
                custom_data['message'] = "Followed"
            custom_data.update(serializer.data)
            return Response(custom_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

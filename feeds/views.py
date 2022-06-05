from rest_framework.generics import GenericAPIView, ListAPIView
from feeds.mixins import HomeFeedPostsListMixin
from feeds.models import Follower, Post
from feeds.serializers import FollowerSerializer, GetNetworkSerializer, GetPostSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from jobs.models import Job
from users.models import OrganizationProfile, UserProfile

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
                    custom_data['message'] = f"Connected with {follower.being_followed.get_full_name()}"
                else:
                    custom_data['message'] = f"Unconnected with {follower.being_followed.get_full_name()}"
            else:
                serializer.save(follower=self.request.user)
                custom_data['message'] = f"Connected with {serializer.validated_data.get('being_followed').get_full_name()}"
            custom_data.update(serializer.data)
            return Response(custom_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

class GetLandingPageDetails(APIView):
    """ View to register new users in the system """
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        _dict = dict()
        _dict['active_vacancies'] = Job.objects.filter(is_active=True).count()
        _dict['organizations'] = OrganizationProfile.objects.all().count()
        _dict['job_seekers'] = UserProfile.objects.all().count()
        _dict['total_vacancies'] = Job.objects.all().count()
        return Response(_dict, status=status.HTTP_200_OK)
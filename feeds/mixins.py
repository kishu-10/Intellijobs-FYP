from rest_framework.mixins import ListModelMixin, DestroyModelMixin
from rest_framework.response import Response
from feeds.models import Follower, Post
from rest_framework import serializers, status
from feeds.serializers import GetPostSerializer


class HomeFeedPostsListMixin(ListModelMixin):

    def list(self, request, *args, **kwargs):
        followers = request.user.followers.filter(is_active=True)
        being_followed = list()
        for i in followers:
            being_followed.append(i.being_followed.id)
        posts = Post.objects.filter(
            author__id__in=being_followed).order_by('-date_created')
        serializer = GetPostSerializer(posts, many=True, context={'request':self.request})
        data = serializer.data
        return Response(data)


class PostDeleteMixin(DestroyModelMixin):

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.user.is_superuser and request.user.user_type != "staff" and instance.author != request.user:
            raise serializers.ValidationError(
                {"message": "The following post can only be deleted by its author."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"message": "The post has been deleted."}, status=status.HTTP_204_NO_CONTENT)

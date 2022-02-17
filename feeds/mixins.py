from rest_framework.mixins import ListModelMixin, DestroyModelMixin
from rest_framework.response import Response
from feeds.models import Post
from rest_framework import serializers, status
from feeds.serializers import GetPostSerializer


class HomeFeedPostsListMixin(ListModelMixin):

    def list(self, request, *args, **kwargs):
        posts = Post.objects.filter().order_by('-date_created')
        serializer = GetPostSerializer(posts, many=True)
        data = serializer.data
        return Response(data)


class PostDeleteMixin(DestroyModelMixin):

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            raise serializers.ValidationError(
                {"message": "Cannot delete."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"message": "Post deleted."}, status=status.HTTP_204_NO_CONTENT)

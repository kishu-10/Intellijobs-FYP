from rest_framework import serializers

from feeds.models import Like, Post, PostImage, Comment


class PostImageSerializer(serializers.ModelSerializer):
    """ To create, update, list and delete Post Images """

    class Meta:
        model = PostImage
        fields = "__all__"


class LikeSerializer(serializers.ModelSerializer):
    """ To create, update, list and delete Post Likes """

    class Meta:
        model = Like
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    """ To create, update, list and delete Post Comments """

    class Meta:
        model = Comment
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    """ To create, update, list and delete Posts """

    class Meta:
        model = Post
        fields = "__all__"


class GetPostSerializer(serializers.ModelSerializer):
    """ To get the details of Post """

    images = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"

    def get_images(self, obj):
        images = PostImage.objects.filter(post=obj)
        serializer = PostImageSerializer(images, many=True)
        return serializer.data

    def get_likes(self, obj):
        likes = PostImage.objects.filter(post=obj)
        serializer = LikeSerializer(likes, many=True)
        return serializer.data

    def get_comments(self, obj):
        comments = Comment.objects.filter(post=obj)
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

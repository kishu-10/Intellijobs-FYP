from unicodedata import name
from rest_framework import serializers

from feeds.models import Follower, Post
from users.models import OrganizationProfile
from django.contrib.auth import get_user_model

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """ To create, update, list and delete Posts """

    class Meta:
        model = Post
        fields = ["caption", "image"]


class GetPostSerializer(serializers.ModelSerializer):
    """ To get the details of Post """
    image = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    display_picture = serializers.SerializerMethodField()
    date_updated = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"

    def get_image(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url)

    def get_author_name(self, obj):
        if obj.author.has_profile and obj.author.user_type == "Candidate":
            return obj.author.user_profile.get_full_name()
        elif obj.author.has_profile and obj.author.user_type == "Organization":
            return obj.author.org_profile.name
        return None

    def get_display_picture(self, obj):
        request = self.context.get('request')
        if obj.author.has_profile and obj.author.user_type == "Candidate" and obj.author.user_profile.display_picture:
            return request.build_absolute_uri(obj.author.user_profile.display_picture.url)
        elif obj.author.has_profile and obj.author.user_type == "Organization" and obj.author.org_profile.display_picture:
            return request.build_absolute_uri(obj.author.org_profile.display_picture.url)
        return None

    def get_date_updated(self, obj):
        return obj.date_updated.strftime("%b %d, %Y")


class FollowerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follower
        fields = ["being_followed"]


class GetFollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = "__all__"


class GetNetworkSerializer(serializers.ModelSerializer):
    """ To get list of organization for network connections """

    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    display_picture = serializers.SerializerMethodField()
    has_followed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "user_uuid", "name", "description",
                  "display_picture", "user_type", "has_followed"]

    def get_name(self, obj):
        if obj.user_type == "Candidate":
            return obj.user_profile.get_full_name()
        elif obj.user_type == "Organization":
            return obj.org_profile.name
        return "Staff User"

    def get_description(self, obj):
        if obj.user_type == "Candidate":
            return "Candidate"
        elif obj.user_type == "Organization":
            return obj.org_profile.org_description
        return "Staff User"

    def get_display_picture(self, obj):
        request = self.context.get('request')
        if obj.user_type == "Candidate" and obj.has_profile and obj.user_profile.display_picture:
            return request.build_absolute_uri(obj.user_profile.display_picture.url)
        elif obj.user_type == "Organization" and obj.has_profile and obj.org_profile.display_picture:
            return request.build_absolute_uri(obj.org_profile.display_picture.url)
        return None

    def get_has_followed(self, obj):
        request = self.context.get('request')
        if Follower.objects.filter(follower=request.user, being_followed=obj, is_active=True).exists():
            return True
        else:
            return False

from rest_framework import serializers

from feeds.models import Follower, Post
from users.models import OrganizationProfile
from django.contrib.auth import get_user_model

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """ To create, update, list and delete Posts """

    class Meta:
        model = Post
        fields = "__all__"


class GetPostSerializer(serializers.ModelSerializer):
    """ To get the details of Post """

    class Meta:
        model = Post
        fields = "__all__"


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
from datetime import date
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from jobs.models import *
from django.utils.translation import ugettext_lazy as _


class CategorySerializer(serializers.ModelSerializer):
    job_count = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    job_name = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = "__all__"

    def get_image(self, category):
        request = self.context.get('request')
        image_url = category.image.url
        return request.build_absolute_uri(image_url)

    def get_job_count(self, obj):
        job = Job.objects.filter(category=obj, deadline__gte=date.today())
        return job.count()

    def get_job_name(self, obj):
        job_name = obj.name.replace(" ", "")
        return job_name


class JobCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'is_active', 'image']
        validators = [
            UniqueTogetherValidator(
                queryset=Category.objects.all(),
                fields=['name']
            )
        ]


class JobSerializer(serializers.ModelSerializer):
    date_created = serializers.SerializerMethodField()
    job_address = serializers.SerializerMethodField()
    organization = serializers.SerializerMethodField()
    organization_picture = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            'id',
            'title',
            'no_of_vacancy',
            'employment_type',
            'experienced_required',
            'deadline',
            'date_created',
            'job_address',
            'job_level',
            'organization',
            'organization_picture'
        ]

    def get_date_created(self, obj):
        return obj.date_created.strftime("%b %d, %Y")

    def get_job_address(self, obj):
        if obj.job_address:
            return obj.job_address
        elif obj.organization.area:
            return obj.organization.area
        elif obj.organization.city:
            return obj.organization.city

    def get_organization(self, obj):
        return obj.organization.name

    def get_organization_picture(self, obj):
        request = self.context.get('request')
        if obj.organization.display_picture:
            return request.build_absolute_uri(obj.organization.display_picture.url)
        else:
            return None


class JobDetailSerializer(serializers.ModelSerializer):
    """Serializer class that returns all the details of a Job"""
    category = CategorySerializer()
    job_address = serializers.SerializerMethodField()
    organization = serializers.SerializerMethodField()
    org_description = serializers.SerializerMethodField()
    is_wishlist = serializers.SerializerMethodField()
    has_applied = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = "__all__"

    def get_organization(self, obj):
        return obj.organization.name

    def get_org_description(self, obj):
        return obj.organization.org_description

    def get_job_address(self, obj):
        if obj.job_address:
            return obj.job_address
        elif obj.organization.area:
            return obj.organization.area
        elif obj.organization.city:
            return obj.organization.city

    def get_is_wishlist(self, obj):
        request = self.context.get('request')
        wishlist = JobWishlist.objects.filter(
            owner=request.user.user_profile).first()
        if wishlist:
            details = wishlist.wishlist_detail.filter(is_active=True)
            job_wishlist = list()
            for i in details:
                job_wishlist.append(i.job)
            if obj in job_wishlist:
                return True
        return False

    def get_has_applied(self, obj):
        request = self.context.get('request')
        if JobApplication.objects.filter(candidate=request.user.user_profile, job=obj).exists():
            return True
        return False


class GetJobWishListSerializer(serializers.ModelSerializer):
    jobs = serializers.SerializerMethodField()

    class Meta:
        model = JobWishlist
        fields = "__all__"

    def get_jobs(self, obj):
        request = self.context.get('request')
        jobs = obj.wishlist_detail.filter(is_active=True)
        job_list = list()
        for i in jobs:
            job_list.append(i.job)
        serializer = JobSerializer(
            job_list, many=True, context={'request': request})
        return serializer.data


class JobWishListDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobWishlistDetail
        fields = ["job"]


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ["cv", "job"]
        extra_kwargs = {'job': {'required': True},
                        'cv': {'required': True}}

    def validate(self, attrs):
        request = self.context.get('request')
        if JobApplication.objects.filter(job=attrs.get(
                'job'), candidate=request.user.user_profile).exists():
            raise serializers.ValidationError({"message": "Already applied"})
        return super().validate(attrs)


class GetJobApplicationSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    date_created = serializers.SerializerMethodField()
    class Meta:
        model = JobApplication
        fields = "__all__"

    def get_date_created(self, obj):
        return obj.date_created.strftime("%b %d, %Y")
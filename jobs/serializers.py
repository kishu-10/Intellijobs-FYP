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
    category = CategorySerializer(read_only=True)
    date_created = serializers.SerializerMethodField()
    job_address = serializers.SerializerMethodField()
    class Meta:
        model = Job
        fields = [
            'id',
            'title',
            'no_of_vacancy',
            'employment_type',
            'experienced_required',
            'deadline',
            'category',
            'date_created',
            'job_address',
            'job_level'
        ]
    
    def get_date_created(self, obj):
        return obj.date_created.strftime("%b %d, %Y")

    def get_job_address(self, obj):
        if obj.job_address:
            return obj.job_address
        elif obj.organization.city:
            return obj.organization.city
        elif obj.organization.area:
            return obj.organization.area

class JobDetailSerializer(serializers.ModelSerializer):
    """Serializer class that returns all the details of a Job"""
    category = CategorySerializer()
    organization = serializers.SerializerMethodField()
    class Meta:
        model = Job
        fields = "__all__"

    def get_organization(self, obj):
        return obj.organization.name

from datetime import date
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from vacancy.models import *
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

    class Meta:
        model = Job
        fields = [
            'id',
            'title',
            'no_of_vacancy',
            'employment_type',
            'experienced_required',
            'deadline',
            'category'
        ]


class JobDetailSerializer(serializers.ModelSerializer):
    """Serializer class that returns all the details of a Job"""
    category = CategorySerializer()

    class Meta:
        model = Job
        fields = "__all__"
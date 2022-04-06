from rest_framework.mixins import CreateModelMixin
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class CreateResumeMixin(CreateModelMixin):

    def perform_create(self, serializer):
        try:
            profile = User.objects.get(
                pk=self.request.data.get('user_id')).user_profile
        except Exception:
            profile = None
            raise serializers.ValidationError(
                {"message": "User profile does not exists"})
        if profile:
            serializer.save(profile=profile)


class CreateExperienceMixin(CreateModelMixin):

    def perform_create(self, serializer):
        try:
            resume = self.request.user.user_profile.resume
        except Exception:
            resume = None
            raise serializers.ValidationError(
                {"message": "Resume for user does not exists"})
        if resume:
            serializer.save(resume=resume)


class CreateSkillMixin(CreateModelMixin):

    def perform_create(self, serializer):
        try:
            resume = self.request.user.user_profile.resume
        except Exception:
            resume = None
            raise serializers.ValidationError(
                {"message": "Resume for user does not exists"})
        if resume:
            serializer.save(resume=resume)


class CreateEducationMixin(CreateModelMixin):

    def perform_create(self, serializer):
        try:
            resume = self.request.user.user_profile.resume
        except Exception:
            resume = None
            raise serializers.ValidationError(
                {"message": "Resume for user does not exists"})
        if resume:
            serializer.save(resume=resume)


class CreateAchievementMixin(CreateModelMixin):

    def perform_create(self, serializer):
        try:
            resume = self.request.user.user_profile.resume
        except Exception:
            resume = None
            raise serializers.ValidationError(
                {"message": "Resume for user does not exists"})
        if resume:
            serializer.save(resume=resume)

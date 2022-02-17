from rest_framework.mixins import CreateModelMixin
from rest_framework import serializers, status


class CreateResumeMixin(CreateModelMixin):

    def perform_create(self, serializer):
        try:
            profile = self.user.user_profile
        except Exception:
            profile = None
            raise serializers.ValidationError(
                {"message": "User profile does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        if profile:
            serializer.save(profile=profile)


class CreateExperienceMixin(CreateModelMixin):

    def perform_create(self, serializer):
        try:
            resume = self.user.user_profile.resume
        except Exception:
            resume = None
            raise serializers.ValidationError(
                {"message": "Resume for user does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        if resume:
            serializer.save(resume=resume)


class CreateSkillMixin(CreateModelMixin):

    def perform_create(self, serializer):
        try:
            resume = self.user.user_profile.resume
        except Exception:
            resume = None
            raise serializers.ValidationError(
                {"message": "Resume for user does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        if resume:
            serializer.save(resume=resume)


class CreateEducationMixin(CreateModelMixin):

    def perform_create(self, serializer):
        try:
            resume = self.user.user_profile.resume
        except Exception:
            resume = None
            raise serializers.ValidationError(
                {"message": "Resume for user does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        if resume:
            serializer.save(resume=resume)


class CreateAchievementMixin(CreateModelMixin):

    def perform_create(self, serializer):
        try:
            resume = self.user.user_profile.resume
        except Exception:
            resume = None
            raise serializers.ValidationError(
                {"message": "Resume for user does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        if resume:
            serializer.save(resume=resume)


class CreateLanguageMixin(CreateModelMixin):

    def perform_create(self, serializer):
        try:
            resume = self.user.user_profile.resume
        except Exception:
            resume = None
            raise serializers.ValidationError(
                {"message": "Resume for user does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        if resume:
            serializer.save(resume=resume)

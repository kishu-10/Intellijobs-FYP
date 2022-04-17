from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework import serializers, status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from cvbuilder.models import Education, Experience, Resume, Skill

from cvbuilder.serializers import EducationSerializer, ExperienceSerializer, ResumeSerializer, SkillSerializer


User = get_user_model()


class CreateResumeMixin(CreateModelMixin):

    def perform_create(self, serializer):
        try:
            profile = User.objects.get(
                user_uuid=self.request.data.get('user_id')).user_profile
        except Exception:
            profile = None
            raise serializers.ValidationError(
                {"message": "User profile does not exists"})
        if profile:
            serializer.save(profile=profile)


class CreateExperienceMixin(CreateModelMixin):

    def create(self, request, *args, **kwargs):
        try:
            resume = self.request.user.user_profile.resume
        except Exception:
            resume = None
            raise serializers.ValidationError(
                {"message": "Resume for user does not exists"})
        data = request.data.get('experiences')
        for i in data:
            if i.get('id'):
                education = Experience.objects.filter(pk=i.get('id'))
                i.pop('id')
                if not i.get('end_date'):
                    i.pop('end_date')
                education.update(**i)
            else:
                if not i.get('end_date'):
                    i.pop('end_date')
                Experience.objects.create(**i, resume=resume)
        return Response(request.data, status=status.HTTP_201_CREATED)


class CreateSkillMixin(CreateModelMixin):

    def create(self, request, *args, **kwargs):
        try:
            resume = self.request.user.user_profile.resume
        except Exception:
            resume = None
            raise serializers.ValidationError(
                {"message": "Resume for user does not exists"})
        data = request.data.get('skills')
        for i in data:
            if i.get('id'):
                education = Skill.objects.filter(pk=i.get('id'))
                i.pop('id')
                education.update(**i)
            else:
                Skill.objects.create(**i, resume=resume)
        return Response(request.data, status=status.HTTP_201_CREATED)


class CreateEducationMixin(CreateModelMixin):
    def create(self, request, *args, **kwargs):
        try:
            resume = self.request.user.user_profile.resume
        except Exception:
            resume = None
            raise serializers.ValidationError(
                {"message": "Resume for user does not exists"})
        data = request.data.get('educations')
        for i in data:
            if i.get('id'):
                education = Education.objects.filter(pk=i.get('id'))
                i.pop('id')
                if not i.get('end_date'):
                    i.pop('end_date')
                education.update(**i)
            else:
                if not i.get('end_date'):
                    i.pop('end_date')
                Education.objects.create(**i, resume=resume)
        return Response(request.data, status=status.HTTP_201_CREATED)


class ListResumeMixin(ListModelMixin):

    def list(self, request, *args, **kwargs):
        super().list(request, *args, **kwargs)
        try:
            resume = self.request.user.user_profile
        except Exception:
            resume = None
        resumes = None
        if resume:
            resumes = Resume.objects.filter(
                profile=self.request.user.user_profile)
        serializer = ResumeSerializer(resumes, many=True)
        return Response(serializer.data)


class ListEducationMixin(ListModelMixin):

    def list(self, request, *args, **kwargs):
        super().list(request, *args, **kwargs)
        try:
            resume = self.request.user.user_profile.resume
        except Exception:
            resume = None
        educations = None
        if resume:
            educations = Education.objects.filter(
                resume=self.request.user.user_profile.resume)
        serializer = EducationSerializer(educations, many=True)
        return Response(serializer.data)


class ListExperienceMixin(ListModelMixin):

    def list(self, request, *args, **kwargs):
        super().list(request, *args, **kwargs)
        try:
            resume = self.request.user.user_profile.resume
        except Exception:
            resume = None
        experiences = None
        if resume:
            experiences = Experience.objects.filter(
                resume=self.request.user.user_profile.resume)
        serializer = ExperienceSerializer(experiences, many=True)
        return Response(serializer.data)


class ListSkillMixin(ListModelMixin):

    def list(self, request, *args, **kwargs):
        super().list(request, *args, **kwargs)
        try:
            resume = self.request.user.user_profile.resume
        except Exception:
            resume = None
        skills = None
        if resume:
            skills = Skill.objects.filter(
                resume=self.request.user.user_profile.resume)
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)

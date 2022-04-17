from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .mixins import *
from .models import *
from .serializers import *


# Create your views here.

class ResumeViewset(ModelViewSet, ListResumeMixin, CreateResumeMixin):
    serializer_class = ResumeSerializer
    queryset = Resume.objects.all()


class ExperienceViewset(ModelViewSet, ListExperienceMixin, CreateExperienceMixin):
    serializer_class = ExperienceSerializer
    queryset = Experience.objects.all()


class SkillViewset(ModelViewSet, ListSkillMixin, CreateSkillMixin):
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()


class EducationViewset(ModelViewSet, ListEducationMixin, CreateEducationMixin):
    serializer_class = EducationSerializer
    queryset = Education.objects.all()


class CreateEducationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = EducationSerializer(data=request.data)
        if serializer.is_valid():
            Education.objects.update_or_create()

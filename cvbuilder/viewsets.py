from rest_framework.viewsets import ModelViewSet

from .mixins import *
from .models import *
from .serializers import *


# Create your views here.

class ResumeViewset(ModelViewSet, CreateResumeMixin):
    serializer_class = ResumeSerializer
    queryset = Resume.objects.all()


class ExperienceViewset(ModelViewSet, CreateExperienceMixin):
    serializer_class = ExperienceSerializer
    queryset = Experience.objects.all()


class SkillViewset(ModelViewSet, CreateSkillMixin):
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()


class EducationViewset(ModelViewSet, CreateEducationMixin):
    serializer_class = EducationSerializer
    queryset = Education.objects.all()


class AchievementViewset(ModelViewSet, CreateAchievementMixin):
    serializer_class = AchievementSerializer
    queryset = Achievement.objects.all()


class LanguageViewset(ModelViewSet, CreateLanguageMixin):
    serializer_class = ResumeSerializer
    queryset = Language.objects.all()

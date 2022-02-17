from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import *

router = DefaultRouter()
router.register(r"resume/", ResumeViewset, basename="resume")
router.register(r"experience/", ExperienceViewset, basename="experience")
router.register(r"skill/", SkillViewset, basename="skill")
router.register(r"education/", EducationViewset, basename="education")
router.register(r"achivement/", AchievementViewset, basename="achievement")
router.register(r"language/", LanguageViewset, basename="language")

urlpatterns = [
    path("", include(router.urls))
]

from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .viewsets import *

app_name = "cvbuilder"

router = SimpleRouter()
router.register("resume", ResumeViewset, basename="resume")
router.register("experience", ExperienceViewset, basename="experience")
router.register("skill", SkillViewset, basename="skill")
router.register("education", EducationViewset, basename="education")
router.register("achivement", AchievementViewset, basename="achievement")

urlpatterns = [
    path("", include(router.urls))
]
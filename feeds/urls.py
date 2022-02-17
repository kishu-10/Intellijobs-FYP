from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import *

router = DefaultRouter()
router.register(r"image/", PostImageViewSet, basename="post_images")
router.register(r"like/", LikeViewSet, basename="post_likes")
router.register(r"comment/", CommentViewSet, basename="post_comments")

urlpatterns = [
    path("", include(router.urls))
]

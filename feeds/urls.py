from django.urls import include, path
from rest_framework.routers import SimpleRouter

from feeds.views import CreateNetworkView, GetNetworksView

from .viewsets import *

app_name = "feeds"

router = SimpleRouter()
router.register("posts", PostViewSet, basename="posts")

urlpatterns = [
    path("", include(router.urls)),
    path("networks/", GetNetworksView.as_view(), name="networks_list"),
    path("networks/add/", CreateNetworkView.as_view(), name="networks_add")
]

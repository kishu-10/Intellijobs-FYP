from django.urls import include, path
from rest_framework.routers import DefaultRouter

from feeds.views import CreateNetworkView, GetNetworksView

from .viewsets import *

router = DefaultRouter()

app_name = "feeds"

urlpatterns = [
    path("", include(router.urls)),
    path("networks/", GetNetworksView.as_view(), name="networks_list"),
    path("networks/add/", CreateNetworkView.as_view(), name="networks_add")
]

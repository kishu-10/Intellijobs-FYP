from django.urls import path
from jobs.views import (DashboardJobCategoryCreateView,
                        DashboardJobCategoryDeleteView,
                        DashboardJobCategoryListView,
                        DashboardJobCategoryUpdateView, DashboardJobCreateView,
                        DashboardJobDeleteView, DashboardJobListView,
                        DashboardJobUpdateView)

from dashboard.views import DashboardIndexView

app_name = "dashboard"

urlpatterns = [
    path("", DashboardIndexView.as_view(), name="index"),

    # Jobs
    path("jobs/", DashboardJobListView.as_view(), name="jobs_list"),
    path("jobs/create/", DashboardJobCreateView.as_view(), name="jobs_create"),
    path("jobs/<int:pk>-update/",
         DashboardJobUpdateView.as_view(), name="jobs_update"),
    path("jobs/<int:pk>-delete/",
         DashboardJobDeleteView.as_view(), name="jobs_delete"),

    # Job Category
    path("jobs/job-categories/",
         DashboardJobCategoryListView.as_view(), name="category_list"),
    path("jobs/job-category/create/",
         DashboardJobCategoryCreateView.as_view(), name="category_create"),
    path("jobs/job-category/<int:pk>-update/",
         DashboardJobCategoryUpdateView.as_view(), name="category_update"),
    path("jobs/job-category/<int:pk>-delete/",
         DashboardJobCategoryDeleteView.as_view(), name="category_delete"),
]

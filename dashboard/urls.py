from django.urls import path

from dashboard.views import DashboardIndexView
from jobs.views import DashboardJobCategoryCreateView, DashboardJobCategoryDeleteView, DashboardJobCategoryListView, DashboardJobCategoryUpdateView

app_name = "dashboard"

urlpatterns = [
    path("", DashboardIndexView.as_view(), name="index"),
    path("jobs/job-category/list/",
         DashboardJobCategoryListView.as_view(), name="category_list"),
    path("jobs/job-category/create/",
         DashboardJobCategoryCreateView.as_view(), name="category_create"),
    path("jobs/job-category/<int:pk>-update/",
         DashboardJobCategoryUpdateView.as_view(), name="category_update"),
    path("jobs/job-category/<int:pk>-delete/",
         DashboardJobCategoryDeleteView.as_view(), name="category_delete"),
]

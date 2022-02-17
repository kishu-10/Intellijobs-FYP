from django.conf.urls import url
from django.urls import re_path
from django.urls.conf import path

from jobs.views import *

urlpatterns = [
    path('jobs/', JobListView.as_view(), name='job-list'),
    path('job/detail/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('categories/', CategoriesListView.as_view(), name='job-category'),
    path('category/create/',CategoryCreateView.as_view(),name='job-category-create'),
  
]

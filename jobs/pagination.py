from rest_framework.pagination import PageNumberPagination
from rest_framework.utils.urls import remove_query_param, replace_query_param


class JobPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "job_page"
    max_page_size = 20000
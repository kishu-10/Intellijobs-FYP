from functools import partial
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from dashboard.mixins import DashboardUserMixin
from feeds.serializers import User
from jobs.forms import CategoryForm, JobForm
from jobs.serializers import *
from rest_framework import status
from django.views.generic import CreateView, ListView, UpdateView, View, DetailView
from django.contrib import messages
from django.db.models import Q

# Create your views here.

# Dashboard side


class DashboardJobCategoryCreateView(DashboardUserMixin, CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy("dashboard:category_list")
    template_name = "job-category/category-create.html"

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        messages.success(
            self.request, f"{name} created successfully.")
        super().form_valid(form)
        return HttpResponseRedirect(self.success_url)


class DashboardJobCategoryListView(DashboardUserMixin, ListView):
    model = Category
    template_name = "job-category/category-list.html"
    context_object_name = "category_list"


class DashboardJobCategoryUpdateView(DashboardUserMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "job-category/category-update.html"
    context_object_name = "category"
    success_url = reverse_lazy("dashboard:category_list")

    def form_valid(self, form):
        messages.success(
            self.request, f"{self.object.name} updated successfully.")
        super().form_valid(form)
        return HttpResponseRedirect(self.success_url)


class DashboardJobCategoryDeleteView(DashboardUserMixin, View):
    success_url = reverse_lazy("dashboard:category_list")

    def post(self, request, *args, **kwargs):
        category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        category.delete()
        messages.success(
            self.request, f"{category.name} deleted successfully.")
        return HttpResponseRedirect(self.success_url)


class DashboardJobCreateView(DashboardUserMixin, CreateView):
    model = Job
    form_class = JobForm
    success_url = reverse_lazy("dashboard:jobs_list")
    template_name = "jobs/jobs-create.html"

    def form_valid(self, form):
        title = form.cleaned_data.get('title')
        instance = form.save(commit=False)
        instance.organization = self.request.user.org_profile
        instance.save()
        messages.success(
            self.request, f"{title} created successfully.")
        return HttpResponseRedirect(self.success_url)


class DashboardJobListView(DashboardUserMixin, ListView):
    model = Job
    template_name = "jobs/jobs-list.html"
    context_object_name = "jobs_list"

    def get_queryset(self):
        if self.request.user.user_type == "Organization":
            org_profile = self.request.user.org_profile
            queryset = Job.objects.filter(organization=org_profile)
        else:
            queryset = Job.objects.order_by('-date_created')
        return queryset


class DashboardJobUpdateView(DashboardUserMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/jobs-update.html"
    context_object_name = "job"
    success_url = reverse_lazy("dashboard:jobs_list")

    def form_valid(self, form):
        messages.success(
            self.request, f"{self.object.title} updated successfully.")
        super().form_valid(form)
        return HttpResponseRedirect(self.success_url)


class DashboardJobDeleteView(DashboardUserMixin, View):
    success_url = reverse_lazy("dashboard:jobs_list")

    def post(self, request, *args, **kwargs):
        job = get_object_or_404(Job, pk=self.kwargs.get('pk'))
        job.delete()
        messages.success(
            self.request, f"{job.title} deleted successfully.")
        return HttpResponseRedirect(self.success_url)


class DashboardCandidateJobApplicationListView(DashboardUserMixin, DetailView):
    model = Job
    context_object_name = "job"
    template_name = "jobs/candidate-applications.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applications'] = JobApplication.objects.filter(
            job=self.object).order_by('-date_created', '-id')
        return context


# API
class JobListView(ListAPIView):
    serializer_class = JobSerializer
    queryset = Job.objects.filter(
        is_active=True).order_by('-date_created')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', None)
        title = self.request.query_params.get('title', None)
        address = self.request.query_params.get('address', None)
        if category:
            queryset = queryset.filter(category=category)
        if title and address:
            queryset.filter(Q(title__iexact=title) | Q(job_address__iexact=address) | Q(
                organization__city__iexact=address) | Q(organization__area__iexact=address))
        elif title and not address:
            queryset.filter(title__iexact=title)
        elif address and not title:
            queryset.filter(Q(job_address__iexact=address) | Q(
                organization__city__iexact=address) | Q(organization__area__iexact=address))
        return queryset[0:9]


class CategoriesListView(APIView):

    def get(self, request):
        """API to fetch all the Job Categories"""
        categories = Category.objects.filter(is_active=True)
        serializer = CategorySerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)


class JobDetailView(APIView):

    def get(self, request, pk):
        try:
            job = Job.objects.get(pk=pk)
        except:
            return Response([],
                            status=status.HTTP_400_BAD_REQUEST
                            )
        serializer = JobDetailSerializer(job, context={'request': request})
        return Response(serializer.data)


class CategoryCreateView(APIView):

    def post(self, request):
        serializer = JobCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetJobWishListView(APIView):

    def get(self, request, *args, **kwargs):
        """API to fetch all the Wishlist Jobs"""
        user = User.objects.get(user_uuid=self.kwargs.get('uuid'))
        wishlist = JobWishlist.objects.filter(owner=user.user_profile).first()
        serializer = GetJobWishListSerializer(
            wishlist, context={'request': request})
        return Response(serializer.data)

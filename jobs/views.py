import collections
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from cvbuilder.models import Resume, Skill
from dashboard.mixins import DashboardUserMixin
from feeds.models import Follower
from feeds.serializers import User
from jobs.forms import CategoryForm, JobForm
from jobs.pagination import JobPagination
from jobs.recommendation import get_recommended_jobs, match_location
# from jobs.recommendation import match_job
from jobs.serializers import *
from rest_framework import status
from django.views.generic import CreateView, ListView, UpdateView, View, DetailView
from django.contrib import messages
from django.db.models import Q
from django.template.loader import render_to_string
from intellijobs.tasks import send_email_verfication

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

        # send vacancy announcement to followers
        org_profile = self.request.user.org_profile
        followers_email = list()
        followers = Follower.objects.filter(
            being_followed=self.request.user, is_active=True)
        for i in followers:
            followers_email.append(i.follower.email)
        if org_profile.display_picture:
            logo = self.request.build_absolute_uri(
                org_profile.display_picture.url)
        else:
            logo = self.request.build_absolute_uri(
                '/static/assets/images/logo.png')
        subject = "New Job Vacancy Announcement - IntelliJobs"
        for i in followers_email:
            message = render_to_string('email-templates/job-open-email.html', {
                'email': i,
                'domain': "localhost:3000/job/",
                'logo': logo,
                'organization': org_profile,
                'job': instance
            })
            send_email_verfication.delay(
                subject, message, i)
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
            job=self.object, status="Pending").order_by('-date_created', '-id')
        return context


class DashboardApproveCandidateView(DashboardUserMixin, View):
    def get(self, request, *args, **kwargs):
        candidate = get_object_or_404(
            UserProfile, pk=self.kwargs.get('candidate'))
        job = get_object_or_404(Job, pk=self.kwargs.get('job'))
        application = JobApplication.objects.get(job=job, candidate=candidate)
        application.status = "Approved"
        application.save()
        messages.success(
            request, f"{candidate.get_full_name()} approved successfully.")
        return redirect(request.META.get('HTTP_REFERER'))


class DashboardRejectCandidateView(DashboardUserMixin, View):
    def get(self, request, *args, **kwargs):
        candidate = get_object_or_404(
            UserProfile, pk=self.kwargs.get('candidate'))
        job = get_object_or_404(Job, pk=self.kwargs.get('job'))
        application = JobApplication.objects.get(job=job, candidate=candidate)
        application.status = "Rejected"
        application.save()
        messages.success(
            request, f"{candidate.get_full_name()} rejected successfully.")
        return redirect(request.META.get('HTTP_REFERER'))


# API
class JobListView(ListAPIView):
    serializer_class = JobSerializer
    queryset = Job.objects.filter(
        is_active=True).order_by('-date_created')
    pagination_class = JobPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        skills_list = []
        location_job = []
        recommended_jobs = []

        """
        sort list of jobs matching user's resume skills 
        and job skills 
        """
        try:
            resume = Resume.objects.get(profile=user.user_profile)
        except Exception:
            resume = None
        if resume:
            skills = Skill.objects.filter(resume=resume)

            for i in skills:
                skills_list.append(i.title)
            job_list = []
            for job in queryset:
                match_value = get_recommended_jobs(
                    [job.skills], [' '.join(skills_list)])
                job_list.append(
                    {"match_value": match_value.tolist()[0][0], "job": job})
            ordered_jobs = sorted(
                job_list, key=lambda d: d["match_value"], reverse=True)
            for i in ordered_jobs:
                recommended_jobs.append(i['job'])

        """
        sort list of jobs matching user profile location 
        and organization profile location 
        """
        try:
            profile = self.request.user.user_profile
        except Exception:
            profile = None
            raise serializers.ValidationError(
                {'message': 'User profile does not exist'})

        job_location_list = []
        if resume:
            for job in recommended_jobs:
                location_match_value = match_location([job.organization.get_address_detail], [
                                                      profile.get_address_detail])
                job_location_list.append(
                    {"match_value": location_match_value.tolist()[0][0], "job": job})
            ordered_jobs_location = sorted(
                job_location_list, key=lambda d: d["match_value"], reverse=True)
            for i in ordered_jobs_location:
                location_job.append(i['job'])
        else:
            for job in queryset:
                location_match_value = match_location([job.organization.get_address_detail], [
                                                      profile.get_address_detail])
                job_location_list.append(
                    {"match_value": location_match_value.tolist()[0][0], "job": job})
            ordered_jobs_location = sorted(
                job_location_list, key=lambda d: d["match_value"], reverse=True)
            for i in ordered_jobs_location:
                location_job.append(i['job'])
        return location_job


class JobSearchFilterView(APIView):
    pagination_class = JobPagination

    def post(self, request, *args, **kwargs):
        data = request.data
        title = data.get('title')
        address = data.get('address')
        category = data.get('category')
        queryset = Job.objects.filter(
            is_active=True).order_by('-date_created')
        if category:
            queryset = queryset.filter(category=category)
        if title:
            queryset = queryset.filter(title__icontains=title)
        if address:
            queryset = queryset.filter(Q(organization__province__name__icontains=address) | Q(organization__district__name__icontains=address) | Q(
                organization__area__icontains=address) | Q(organization__city__icontains=address) | Q(organization__description__icontains=address))
        serializer = JobSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)


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


class CreateJobWishListView(APIView):

    def post(self, request):
        serializer = JobWishListDetailSerializer(data=request.data)
        custom_data = {}
        if serializer.is_valid():
            try:
                wishlist = JobWishlist.objects.get(
                    owner=self.request.user.user_profile)
            except Exception:
                wishlist = JobWishlist.objects.create(
                    owner=self.request.user.user_profile)
            if JobWishlistDetail.objects.filter(wishlist=wishlist, job=serializer.validated_data.get('job')).exists():
                wishlist_detail = JobWishlistDetail.objects.get(
                    wishlist=wishlist, job=serializer.validated_data.get('job'))
                wishlist_detail.is_active = not wishlist_detail.is_active
                wishlist_detail.save()
                if wishlist_detail.is_active:
                    custom_data['message'] = "Job added to wishlist"
                else:
                    custom_data['message'] = "Job removed from wishlist"
            else:
                serializer.save(wishlist=wishlist)
                custom_data['message'] = "Job added to wishlist"
            custom_data.update(serializer.data)
            return Response(custom_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class JobApplicationCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = JobApplicationSerializer(
            data=request.data, context={"request": request})
        if serializer.is_valid():
            try:
                profile = self.request.user.user_profile
            except Exception:
                profile = None
                raise serializers.ValidationError(
                    {"message": "No user profile"})
            serializer.save(candidate=profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAppliedJobsView(APIView):
    def get(self, request, *args, **kwargs):
        applications = JobApplication.objects.filter(
            candidate=self.request.user.user_profile)
        serializer = GetJobApplicationSerializer(
            applications, many=True, context={'request': request})
        return Response(serializer.data)

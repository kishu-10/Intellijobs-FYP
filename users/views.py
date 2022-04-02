from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from dashboard.mixins import DashboardUserMixin
from users.abstract import Country
from users.forms import OrganizationProfileForm, UserProfileForm
from users.models import OrganizationProfile, UserProfile
from .serializers import *
from rest_framework.generics import ListAPIView
from django.urls import reverse
from django.contrib import messages

User = get_user_model()
account_activation_token = PasswordResetTokenGenerator()


# Django
class VerifyEmail(View):
    """ To Verify Email of Candidate and Organization """

    def get(self, request, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(kwargs.get('uidb64'))
            user = User.objects.get(pk=uid)
        except Exception:
            user = None
        if user and PasswordResetTokenGenerator.check_token(self=account_activation_token, user=user,
                                                            token=kwargs.get('token')):
            user.is_email_verified = True
            user.save()
            if user.user_type == "Organization":
                return redirect(reverse("users:org_profile_create", kwargs={"uuid": user.user_uuid}))
            return redirect(reverse("users:user_profile_create", kwargs={"uuid": user.user_uuid}))
        else:
            return Response({"message": "Invalid Token. Please enter valid token"}, status=status.HTTP_400_BAD_REQUEST)


class CreateUserView(APIView):
    """ View to register new users in the system """

    def post(self, request):
        serializer = UserSerializer(
            data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileCreateView(CreateView):
    """ View to create candidate profile """

    model = UserProfile
    form_class = UserProfileForm
    template_name = "user-profile/user-profile-create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, user_uuid=self.kwargs.get('uuid'))
        context['user'] = user
        return context

    def form_valid(self, form):
        profile = form.save(commit=False)
        user = get_object_or_404(User, user_uuid=self.kwargs.get('uuid'))
        profile.user = user
        profile.country = Country.objects.first()
        profile.save()
        return HttpResponseRedirect("http://localhost:3000/login")


class OrganizationProfileCreateView(CreateView):
    """ View to create organization profile """

    model = OrganizationProfile
    form_class = OrganizationProfileForm
    template_name = "org-profile/org-profile-create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, user_uuid=self.kwargs.get('uuid'))
        context['user'] = user
        return context

    def form_valid(self, form):
        profile = form.save(commit=False)
        user = get_object_or_404(User, user_uuid=self.kwargs.get('uuid'))
        profile.user = user
        profile.country = Country.objects.first()
        profile.save()
        return HttpResponseRedirect("http://localhost:3000/login")


class OrganizationProfileUpdateView(DashboardUserMixin, UpdateView):
    """ View to update organization profile """

    model = OrganizationProfile
    form_class = OrganizationProfileForm
    template_name = "org-profile/org-profile-update.html"
    context_object_name = "organization"

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("dashboard:update_org_profile", kwargs={'pk': self.object.pk})


# Rest Framework
class GetUserDetailsView(APIView):

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs.get('pk'))
        serializer = UserGetSerializer(user, context={'request': self.request})
        return Response(serializer.data)


class GetUserProfileDetailsView(APIView):

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs.get('pk'))
        if user.user_type == "Candidate":
            profile = UserProfile.objects.get(user=user)
            serializer = GetUserProfileSerializer(
                profile, context={'request': self.request})
            return Response(serializer.data)
        return Response([])


class GetProvinceListView(ListAPIView):
    serializer_class = ProvinceSerializer
    queryset = Province.objects.all()


class GetDistrictListView(ListAPIView):
    serializer_class = DistrictSerializer
    queryset = District.objects.all()


class UpdateUserAddressView(APIView):

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs.get('pk'))
        if user.user_type == "Candidate":
            profile = UserProfile.objects.get(user=user)
            serializer = UpdateUserAddressSerializer(profile)
            return Response(serializer.data)
        return Response([])

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs.get('pk'))
        profile = UserProfile.objects.get(user=user)
        serializer = UpdateUserAddressSerializer(
            profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserProfileView(APIView):

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs.get('pk'))
        if user.user_type == "Candidate":
            profile = UserProfile.objects.get(user=user)
            serializer = UpdateUserProfileSerializer(profile)
            return Response(serializer.data)
        return Response([])

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs.get('pk'))
        profile = UserProfile.objects.get(user=user)
        serializer = UpdateUserProfileSerializer(
            profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            if user.email != request.data.get('email'):
                user.email = request.data.get('email')
                user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

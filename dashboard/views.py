from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, View
from intellijobs.tasks import send_email_verfication
from users.models import (OrganizationDocuments, OrganizationProfile,
                          UserProfile)

from .forms import *

User = get_user_model()


# Create your views here
class DashboardIndexView(TemplateView):
    template_name = "index.html"


class DashboardVerifyOrganizationList(ListView):
    model = OrganizationProfile
    queryset = OrganizationProfile.objects.all()
    template_name = "verify-organization/verify-organization-list.html"
    context_object_name = "organizations"


class DashboardVerifyOrganization(View):
    template_name = "verify-organization/verify-organization.html"

    def get(self, request, *args, **kwargs):
        context = dict()
        organization = get_object_or_404(
            OrganizationProfile, pk=self.kwargs.get('pk'))
        org_files = OrganizationDocuments.objects.filter(
            ogranization=organization)
        org_images = []
        org_docs = []
        for i in org_files:
            if i.document.name.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.svg', '.webp')):
                org_images.append(i)
            else:
                org_docs.append(i)
        context['organization'] = organization
        context['org_docs'] = org_docs
        context['org_images'] = org_images
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        organization = get_object_or_404(
            OrganizationProfile, pk=self.kwargs.get('pk'))
        organization.verification_status = "Verified"
        organization.save()
        messages.success(
            self.request, f"{organization.name} verified successfully.")
        return redirect('dashboard:verify_organization_list')


class DashboardRejectOrganizationVerification(View):

    def post(self, request, *args, **kwargs):
        organization = get_object_or_404(
            OrganizationProfile, pk=self.kwargs.get('pk'))
        organization.verification_status = "Rejected"
        organization.save()
        messages.success(
            self.request, f"{organization.name} verification rejected.")
        return redirect("dashboard:verify_organization_list")


class DashboardRegisterStaffListView(ListView):
    model = User
    queryset = User.objects.filter(user_type="Staff")
    template_name = "staff-registration/staff-register-list.html"
    context_object_name = "staffs"


class DashboardRegisterStaffCreateView(CreateView):
    model = User
    form_class = StaffRegistrationForm
    template_name = "staff-registration/staff-register-create.html"
    success_url = reverse_lazy("dashboard:staff_register_list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.user_type = "Staff"
        user.save()
        messages.success(
            self.request, f"{form.cleaned_data.get('username')} created successfully.")
        subject = "Login Credentials for Dashboard - IntelliJobs"
        message = render_to_string('email-templates/staff-login-credentials.html', {
            'url': self.request.build_absolute_uri('/dashboard'),
            'email': form.cleaned_data.get('email'),
            'username': form.cleaned_data.get('username'),
            'password': form.cleaned_data.get('password')
        })

        send_email_verfication.delay(
            subject, message, form.cleaned_data.get('email'))
        print(form.cleaned_data.get('email'))
        return super().form_valid(form)

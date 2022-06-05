from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, View, UpdateView
from dashboard.mixins import DashboardUserMixin
from intellijobs.tasks import send_email_verfication
from jobs.models import Job, JobApplication
from users.models import OrganizationDocuments, OrganizationProfile, UserProfile
from .forms import *

User = get_user_model()


# Create your views here
class DashboardIndexView(DashboardUserMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pending_vacancies'] = JobApplication.objects.filter(status="Pending").count()
        context['organizations'] = OrganizationProfile.objects.all().count()
        context['applied_candidates'] = JobApplication.objects.all().count()
        context['total_vacancies'] = Job.objects.all().count()
        return context


class DashboardVerifyOrganizationList(DashboardUserMixin, ListView):
    model = OrganizationProfile
    queryset = OrganizationProfile.objects.all().order_by('id')
    template_name = "verify-organization/verify-organization-list.html"
    context_object_name = "organizations"


class DashboardVerifyOrganization(DashboardUserMixin, View):
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


class DashboardRejectOrganizationVerification(DashboardUserMixin, View):

    def post(self, request, *args, **kwargs):
        organization = get_object_or_404(
            OrganizationProfile, pk=self.kwargs.get('pk'))
        organization.verification_status = "Rejected"
        organization.save()
        messages.success(
            self.request, f"{organization.name} verification rejected.")
        return redirect("dashboard:verify_organization_list")


class DashboardRegisterStaffListView(DashboardUserMixin, ListView):
    model = User
    queryset = User.objects.filter(user_type="Staff")
    template_name = "staff-registration/staff-register-list.html"
    context_object_name = "staffs"


class DashboardRegisterStaffCreateView(DashboardUserMixin, CreateView):
    model = User
    form_class = StaffRegistrationForm
    template_name = "staff-registration/staff-register-create.html"
    success_url = reverse_lazy("dashboard:staff_register_list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data.get('password'))
        user.user_type = "Staff"
        user.save()
        messages.success(
            self.request, f"{form.cleaned_data.get('username')} created successfully.")
        subject = "Login Credentials for Dashboard - IntelliJobs"
        message = render_to_string('email-templates/staff-login-credentials.html', {
            'url': self.request.build_absolute_uri('/dashboard/'),
            'logo': self.request.build_absolute_uri('/static/assets/images/logo.png'),
            'email': form.cleaned_data.get('email'),
            'username': form.cleaned_data.get('username'),
            'password': form.cleaned_data.get('password')
        })

        send_email_verfication.delay(
            subject, message, form.cleaned_data.get('email'))
        return super().form_valid(form)


class DashboardRegisterStaffUpdateView(DashboardUserMixin, UpdateView):
    model = User
    form_class = StaffRegistrationForm
    template_name = "staff-registration/staff-register-update.html"
    success_url = reverse_lazy("dashboard:staff_register_list")
    context_object_name = "staff"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.set_password(form.cleaned_data.get('password'))
        instance.save()
        user = self.get_object()
        messages.success(
            self.request, f"{user.username} updated successfully.")
        subject = "Login Credentials for Dashboard - IntelliJobs"
        message = render_to_string('email-templates/staff-login-credentials.html', {
            'url': self.request.build_absolute_uri('/dashboard/'),
            'logo': self.request.build_absolute_uri('/static/assets/images/logo.png'),
            'email': form.cleaned_data.get('email'),
            'username': form.cleaned_data.get('username'),
            'password': form.cleaned_data.get('password')
        })
        send_email_verfication.delay(
            subject, message, form.cleaned_data.get('email'))
        return super().form_valid(form)


class DashboardRegisterStaffDeleteView(DashboardUserMixin, View):

    def post(self, request, *args, **kwargs):
        staff = get_object_or_404(User, pk=self.kwargs.get('pk'))
        staff.delete()
        messages.success(
            self.request, f"{staff.username} deleted successfully.")
        return redirect("dashboard:staff_register_list")


class UserLoginDashboardView(View):

    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(user_uuid=self.kwargs.get('uuid'))
            if user.is_superuser or user.has_dashboard_access:
                login(self.request, user)
                return redirect('dashboard:index')
            else:
                return HttpResponseBadRequest()
        except Exception:
            return HttpResponseBadRequest()


class UserLogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect("http://localhost:3000")

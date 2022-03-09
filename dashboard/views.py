from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, View, ListView
from users.models import OrganizationDocuments, OrganizationProfile
from django.contrib.auth import get_user_model
from django.contrib import messages

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
        org_docs = OrganizationDocuments.objects.filter(
            ogranization=organization)
        context['organization'] = organization
        context['org_docs'] = org_docs
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        organization = get_object_or_404(
            OrganizationProfile, user=self.kwargs.get('pk'))
        organization.verification_status = "Verified"
        organization.save()
        messages.success(
            self.request, f"{organization.name} verified successfully.")
        return redirect('dashboard:verify_organization_list')


class DashboardRejectOrganizationVerification(View):

    def post(self, request, *args, **kwargs):
        organization = get_object_or_404(
            OrganizationProfile, user=self.kwargs.get('pk'))
        organization.verification_status = "Rejected"
        organization.save()
        messages.success(
            self.request, f"{organization.name} verification rejected.")
        return redirect("dashboard:verify_organization_list")
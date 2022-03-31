from django.contrib.auth.mixins import LoginRequiredMixin


class StaffUserMixin(LoginRequiredMixin):
    """Verify that the current user is authenticated and staff user."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated and not request.user.is_superuser and not request.user.user_type == "Staff":
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class AdminUserMixin(LoginRequiredMixin):
    """Verify that the current user is authenticated and admin user."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated and not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class DashboardUserMixin(LoginRequiredMixin):
    """Verify that the current user is authenticated and dashboard user."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_anonymous and not request.user.is_authenticated and not request.user.is_superuser and not request.user.user_type == "Staff" and not request.user.user_type == "Organization":
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

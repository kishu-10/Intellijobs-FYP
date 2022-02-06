from rest_framework.permissions import IsAuthenticated


class IsOrganization(IsAuthenticated):
    """ Check if user type is organization or not """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.user_type == "Organization")


class IsStaff(IsAuthenticated):
    """ Check if user type is staff or not """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.user_type == "Staff")

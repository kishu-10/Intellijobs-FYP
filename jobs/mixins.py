from rest_framework.mixins import DestroyModelMixin
from rest_framework import serializers, status


class DestroyJobMixin(DestroyModelMixin):

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.user.is_superuser and request.user.user_type != "staff" and self.request.user.org_profile != instance.organization:
            raise serializers.ValidationError(
                {"message": "Job Vacancy can only be deleted by the author."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().destroy(request, *args, **kwargs)

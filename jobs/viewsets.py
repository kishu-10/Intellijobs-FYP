from rest_framework.viewsets import ModelViewSet
from .mixins import *
from users.permissions import IsOrganization
from .serializers import *

class JobViewsets(ModelViewSet, DestroyJobMixin):
    permission_class = [IsOrganization]
    serializer_class = JobSerializer
    queryset = Job.objects.all()
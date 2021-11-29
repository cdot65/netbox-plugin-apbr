from rest_framework.viewsets import ModelViewSet
from apbr.models import ApbrProfile
from .serializers import ApbrProfileSerializer

class ApbrProfileViewSet(ModelViewSet):
    queryset = ApbrProfile.objects.all()
    serializer_class = ApbrProfileSerializer
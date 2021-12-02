from rest_framework.viewsets import ModelViewSet

from .serializers import ApbrSerializer
from apbr.models import Apbr
from apbr.filters import ApbrFilterSet


class ApbrViewSet(ModelViewSet):
    queryset = Apbr.objects.all()
    serializer_class = ApbrSerializer
    filterset_class = ApbrFilterSet

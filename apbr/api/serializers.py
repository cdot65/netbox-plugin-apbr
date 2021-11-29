from rest_framework.serializers import ModelSerializer
from apbr.models import ApbrProfile

class ApbrProfileSerializer(ModelSerializer):

    class Meta:
        model = ApbrProfile
        fields = ('id', 'name', 'smell')
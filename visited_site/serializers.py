from rest_framework import serializers
from .models import VisitedLink


class VisitedLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitedLink
        fields = ['url']



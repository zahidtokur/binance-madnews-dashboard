from rest_framework import serializers

from core.models import Pair


class AccountSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    secret_key = serializers.CharField(required=True)
    api_key = serializers.CharField(required=True)

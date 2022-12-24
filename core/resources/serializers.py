from rest_framework import serializers

from core.models import Account


class AccountSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=255)
    secret_key = serializers.CharField(required=True, max_length=255)
    api_key = serializers.CharField(required=True, max_length=255)

    def create(self, validated_data):
        return Account.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.secret_key = validated_data.get(
            'secret_key', instance.secret_key)
        instance.api_key = validated_data.get(
            'api_key', instance.api_key)
        instance.save()
        return instance
    
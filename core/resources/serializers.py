from rest_framework import serializers

from core.models import Account
from core.resources.enums import OrderSide, OrderType


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


class OrderSerializer(serializers.Serializer):
    pair = serializers.CharField(required=True)
    multiplier = serializers.FloatField(required=True)
    side = serializers.ChoiceField(
        choices=OrderSide.choices(), default=OrderSide.Long.value)
    type = serializers.ChoiceField(
        choices=OrderType.choices(), default=OrderType.Market.value)

from django.conf import settings
from rest_framework import serializers

from .models import CurrencyExchange, UserBalance


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = settings.AUTH_USER_MODEL.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"]
        )
        UserBalance.objects.create(user=user)
        return user


class CurrencyExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyExchange
        fields = ["id", "currency_code", "rate", "created_at"]
        read_only_fields = ["id", "rate", "created_at"]


class UserBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBalance
        fields = ["balance"]
        read_only_fields = ["balance"]

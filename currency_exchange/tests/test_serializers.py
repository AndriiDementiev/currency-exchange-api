from django.test import TestCase
from django.contrib.auth import get_user_model
from currency_exchange.models import UserBalance, CurrencyExchange
from currency_exchange.serializers import UserBalanceSerializer, CurrencyExchangeSerializer
from decimal import Decimal


User = get_user_model()


class UserBalanceSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.balance = UserBalance.objects.create(user=self.user, balance=500)

    def test_user_balance_serializer(self):
        serializer = UserBalanceSerializer(instance=self.balance)
        self.assertEqual(serializer.data["balance"], 500)


class CurrencyExchangeSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.exchange = CurrencyExchange.objects.create(
            user=self.user, currency_code="USD", rate=Decimal("1.2")
        )

    def test_currency_exchange_serializer(self):
        serializer = CurrencyExchangeSerializer(instance=self.exchange)
        self.assertEqual(serializer.data["currency_code"], "USD")
        self.assertEqual(str(serializer.data["rate"]), "1.2000")

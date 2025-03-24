from django.test import TestCase
from django.contrib.auth import get_user_model
from currency_exchange.models import UserBalance, CurrencyExchange
from decimal import Decimal


User = get_user_model()


class UserBalanceModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.balance = UserBalance.objects.create(user=self.user, balance=100)

    def test_balance_str(self):
        self.assertEqual(str(self.balance), "testuser - 100 coins")

    def test_balance_default_value(self):
        new_user = User.objects.create_user(username="newuser", password="password123")
        balance = UserBalance.objects.create(user=new_user)
        self.assertEqual(balance.balance, 1000)


class CurrencyExchangeModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.exchange = CurrencyExchange.objects.create(
            user=self.user, currency_code="EUR", rate=Decimal("0.85")
        )

    def test_currency_exchange_str(self):
        self.assertEqual(str(self.exchange), "EUR: 0.85 (by testuser)")

    def test_currency_exchange_creation(self):
        self.assertEqual(CurrencyExchange.objects.count(), 1)
        self.assertEqual(self.exchange.currency_code, "EUR")

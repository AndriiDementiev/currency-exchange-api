from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from currency_exchange.models import UserBalance, CurrencyExchange
from decimal import Decimal


User = get_user_model()


class CurrencyExchangeAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

        self.balance = UserBalance.objects.create(user=self.user, balance=10)

    def test_register_user(self):
        response = self.client.post("/api/register/", {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepassword"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(UserBalance.objects.count(), 2)

    def test_get_user_balance(self):
        response = self.client.get("/api/user/balance/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["balance"], 10)

    def test_get_exchange_rate_success(self):
        response = self.client.post("/api/exchange-rate/", {"currency_code": "EUR"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("currency_code", response.data)
        self.assertIn("rate", response.data)

    def test_get_exchange_rate_insufficient_balance(self):
        self.balance.balance = 0
        self.balance.save()
        response = self.client.post("/api/exchange-rate/", {"currency_code": "EUR"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["error"], "Insufficient balance")

    def test_get_exchange_rate_invalid_currency(self):
        response = self.client.post("/api/exchange-rate/", {"currency_code": "INVALID"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_exchange_history(self):
        CurrencyExchange.objects.create(
            user=self.user,
            currency_code="EUR",
            rate=Decimal("0.85")
        )
        CurrencyExchange.objects.create(
            user=self.user,
            currency_code="GBP",
            rate=Decimal("0.75")
        )

        response = self.client.get("/api/exchange-history/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

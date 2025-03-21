from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import (
    generics,
    permissions,
    status
)
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from decimal import Decimal
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter
)

from .models import CurrencyExchange, UserBalance
from .serializers import (
    UserRegistrationSerializer,
    CurrencyExchangeSerializer,
    UserBalanceSerializer
)

@extend_schema(
    summary="Register a new user",
    description="Endpoint for user registration. "
                "Automatically creates a balance for the new user.",
    request=UserRegistrationSerializer,
    responses={201: UserRegistrationSerializer}
)
class RegisterUserView(generics.CreateAPIView):
    queryset = settings.AUTH_USER_MODEL.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(
    summary="Get user balance",
    description="Retrieve the current balance of the authenticated user.",
    responses={200: UserBalanceSerializer}
)
class GetUserBalanceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        balance = get_object_or_404(UserBalance, user=request.user)
        serializer = UserBalanceSerializer(balance)
        return Response(serializer.data)


@extend_schema(
    summary="Get currency exchange rate",
    description="Retrieve the exchange rate for a "
                "specified currency. Costs 1 balance point.",
    request={"type": "object", "properties": {"currency_code": {"type": "string"}}},
    responses={201: CurrencyExchangeSerializer}
)
class GetExchangeRateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        currency_code = request.data.get("currency_code")
        if not currency_code:
            return Response(
                {"error": "Currency code is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_balance = get_object_or_404(UserBalance, user=request.user)

        if user_balance.balance <= 0:
            return Response(
                {"error": "Insufficient balance"},
                status=status.HTTP_403_FORBIDDEN
            )

        exchange_rate_url = (f"{settings.EXCHANGE_RATE_API_URL}/"
                             f"{settings.EXCHANGE_RATE_API_KEY}/latest/USD")

        try:
            response = requests.get(exchange_rate_url)
            response_data = response.json()
            if "conversion_rates" not in response_data:
                return Response(
                    {"error": "Invalid API response"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            rates = response_data["conversion_rates"]
            if currency_code not in rates:
                return Response(
                    {"error": "Invalid currency code"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            exchange_rate = Decimal(str(rates[currency_code]))

            exchange = CurrencyExchange.objects.create(
                user=request.user,
                currency_code=currency_code,
                rate=exchange_rate
            )

            user_balance.balance -= 1
            user_balance.save()

            return Response(
                CurrencyExchangeSerializer(exchange).data,
                status=status.HTTP_201_CREATED
            )

        except requests.RequestException:
            return Response(
                {"error": "External API request failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema_view(
    list=extend_schema(
        summary="List exchange history",
        description="Retrieve the list of past exchange "
                    "requests made by the authenticated user.",
        parameters=[
            OpenApiParameter(
                name="currency",
                description="Filter by currency code",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="date",
                description="Filter by exchange date (YYYY-MM-DD)",
                required=False,
                type=str,
            ),
        ],
    )
)
class GetExchangeHistoryView(generics.ListAPIView):
    serializer_class = CurrencyExchangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = CurrencyExchange.objects.filter(user=self.request.user)

        currency = self.request.query_params.get("currency")
        if currency:
            queryset = queryset.filter(currency_code=currency)

        date = self.request.query_params.get("date")
        if date:
            queryset = queryset.filter(created_at__date=date)

        return queryset

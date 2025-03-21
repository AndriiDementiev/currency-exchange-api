from django.urls import path
from .views import (
    RegisterUserView,
    GetExchangeRateView,
    GetExchangeHistoryView,
    GetUserBalanceView
)


urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    path("currency/", GetExchangeRateView.as_view(), name="currency"),
    path("history/", GetExchangeHistoryView.as_view(), name="history"),
    path("balance/", GetUserBalanceView.as_view(), name="balance"),
]

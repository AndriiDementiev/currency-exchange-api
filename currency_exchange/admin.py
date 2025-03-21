from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import CurrencyExchange, UserBalance

User = get_user_model()

admin.site.unregister(User)


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    list_display = ("id", "username", "email", "date_joined", "is_staff")
    search_fields = ("username", "email")
    list_filter = ("is_staff", "date_joined")
    ordering = ("-date_joined",)


@admin.register(CurrencyExchange)
class CurrencyExchangeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "currency_code", "rate", "created_at")
    search_fields = ("user__username", "currency_code")
    list_filter = ("currency_code", "created_at")
    ordering = ("-created_at",)


@admin.register(UserBalance)
class UserBalanceAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "balance")
    search_fields = ("user__username",)
    ordering = ("-balance",)

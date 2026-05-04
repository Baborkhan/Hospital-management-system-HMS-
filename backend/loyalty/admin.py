from django.contrib import admin
from .models import LoyaltyTransaction

@admin.register(LoyaltyTransaction)
class LoyaltyTransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "transaction_type", "points", "balance_after", "description", "created_at")
    list_filter = ("transaction_type",)
    search_fields = ("user__email", "user__full_name")
    ordering = ("-created_at",)
    readonly_fields = ("balance_after",)

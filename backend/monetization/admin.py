from django.contrib import admin
from .models import Subscription

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("hospital", "plan", "amount", "start_date", "end_date", "is_active")
    list_filter = ("plan", "is_active")
    search_fields = ("hospital__name",)
    list_editable = ("is_active",)

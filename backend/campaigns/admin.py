from django.contrib import admin
from .models import Campaign

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("title", "hospital", "campaign_type", "budget", "start_date", "end_date", "is_active", "impressions", "clicks")
    list_filter = ("campaign_type", "is_active")
    search_fields = ("title", "hospital__name")
    list_editable = ("is_active",)
    readonly_fields = ("impressions", "clicks")

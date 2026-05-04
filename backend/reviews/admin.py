from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("patient", "review_type", "rating", "is_approved", "created_at")
    list_filter = ("review_type", "rating", "is_approved")
    list_editable = ("is_approved",)

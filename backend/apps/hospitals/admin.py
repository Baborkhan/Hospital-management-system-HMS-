from django.contrib import admin
from .models import Hospital, HospitalAdmin, HospitalService

@admin.register(Hospital)
class HospitalAdmin_(admin.ModelAdmin):
    list_display = ("name", "hospital_type", "division", "total_beds", "available_beds",
                    "icu_available", "emergency_open", "rating", "is_verified", "is_premium")
    list_filter = ("hospital_type", "division", "emergency_open", "is_verified", "is_premium")
    search_fields = ("name", "address", "division")
    list_editable = ("available_beds", "icu_available", "emergency_open")
    ordering = ("-rating",)

@admin.register(HospitalService)
class HospitalServiceAdmin(admin.ModelAdmin):
    list_display = ("hospital", "name", "price", "is_available")
    list_filter = ("is_available",)

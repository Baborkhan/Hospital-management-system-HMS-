from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("ref_id", "patient", "doctor", "appointment_date",
                    "time_slot", "visit_type", "status", "fee", "is_paid")
    list_filter = ("status", "visit_type", "is_paid", "appointment_date")
    search_fields = ("ref_id", "patient__user__full_name", "doctor__user__full_name")
    list_editable = ("status", "is_paid")
    date_hierarchy = "appointment_date"

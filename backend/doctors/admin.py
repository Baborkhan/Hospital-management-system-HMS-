from django.contrib import admin
from .models import Doctor, DoctorSchedule

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("__str__", "specialty", "hospital", "consultation_fee",
                    "rating", "is_available_today", "is_verified")
    list_filter = ("specialty", "is_available_today", "is_verified", "accepts_video_consult")
    search_fields = ("user__full_name", "specialty", "bmdc_number")
    list_editable = ("is_available_today",)

@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ("doctor", "day", "start_time", "end_time", "max_slots", "is_active")

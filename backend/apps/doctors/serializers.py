"""Doctor serializers."""
from rest_framework import serializers
from .models import Doctor, DoctorSchedule


class DoctorScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSchedule
        fields = ["day", "start_time", "end_time", "max_slots", "is_active"]


class DoctorListSerializer(serializers.ModelSerializer):
    full_name    = serializers.CharField(source="user.full_name", read_only=True)
    email        = serializers.CharField(source="user.email", read_only=True)
    hospital_name = serializers.CharField(source="hospital.name", read_only=True)
    rating       = serializers.FloatField()

    class Meta:
        model = Doctor
        fields = [
            "id", "full_name", "email", "specialty", "hospital_name",
            "qualification", "experience_years", "consultation_fee", "video_fee",
            "available_days", "languages", "rating", "total_patients",
            "is_verified", "accepts_video_consult", "bmdc_number",
        ]

DoctorSerializer = DoctorListSerializer  # alias for backward compatibility


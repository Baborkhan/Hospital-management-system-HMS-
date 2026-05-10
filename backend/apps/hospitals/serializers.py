"""Hospital serializers."""
from rest_framework import serializers
from .models import Hospital


class HospitalListSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField()

    class Meta:
        model = Hospital
        fields = [
            "id", "name", "hospital_type", "division", "district", "address",
            "phone", "email", "total_beds", "available_beds", "icu_total",
            "icu_available", "emergency_open", "has_pharmacy", "has_lab",
            "has_icu", "specialties", "rating", "rating_count",
            "latitude", "longitude", "is_verified", "is_premium",
        ]


class HospitalDetailSerializer(HospitalListSerializer):
    class Meta(HospitalListSerializer.Meta):
        fields = HospitalListSerializer.Meta.fields + [
            "website", "services", "opening_hours", "established_year",
            "commission_rate", "created_at",
        ]

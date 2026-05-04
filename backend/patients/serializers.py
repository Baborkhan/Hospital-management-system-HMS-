"""Patient serializers."""
from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    full_name   = serializers.CharField(source="user.full_name", read_only=True)
    email       = serializers.CharField(source="user.email", read_only=True)
    phone       = serializers.CharField(source="user.phone", read_only=True)
    age         = serializers.ReadOnlyField()

    class Meta:
        model = Patient
        fields = [
            "id", "full_name", "email", "phone", "patient_id",
            "date_of_birth", "age", "gender", "blood_group",
            "height_cm", "weight_kg", "address", "division",
            "allergies", "chronic_conditions", "current_medications",
            "emergency_contact_name", "emergency_contact_phone",
        ]


class PatientDetailSerializer(PatientSerializer):
    """Extended with all medical fields."""
    class Meta(PatientSerializer.Meta):
        fields = PatientSerializer.Meta.fields + [
            "insurance_provider", "insurance_number", "created_at",
        ]


class MedicalRecordMinimalSerializer(serializers.Serializer):
    id          = serializers.IntegerField()
    record_type = serializers.CharField()
    title       = serializers.CharField()
    created_at  = serializers.DateTimeField()
    doctor_name = serializers.SerializerMethodField()

    def get_doctor_name(self, obj):
        try:
            return obj.doctor.user.full_name if obj.doctor else "N/A"
        except Exception:
            return "N/A"

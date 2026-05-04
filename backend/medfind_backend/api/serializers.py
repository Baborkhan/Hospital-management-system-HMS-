"""
Serializers for API
Convert MongoDB documents to JSON
"""

from rest_framework import serializers
from .models import (
    Hospital, Doctor, Patient, Appointment, LabTest,
    Billing, Pharmacy, MedicalHistory
)


class AddressSerializer(serializers.Serializer):
    street = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    postal_code = serializers.CharField(required=False)
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)


class WorkingHoursSerializer(serializers.Serializer):
    day = serializers.CharField()
    opening_time = serializers.CharField()
    closing_time = serializers.CharField()
    is_closed = serializers.BooleanField()


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)
    
    class Meta:
        model = Doctor
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'


class LabTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTest
        fields = '__all__'


class BillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billing
        fields = '__all__'


class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = '__all__'


class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = '__all__'

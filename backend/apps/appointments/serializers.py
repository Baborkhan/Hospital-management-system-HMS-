from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    doctor_name = serializers.SerializerMethodField()
    patient_name = serializers.SerializerMethodField()
    class Meta:
        model = Appointment
        fields = "__all__"
    def get_doctor_name(self, obj):
        return obj.doctor.user.full_name
    def get_patient_name(self, obj):
        return obj.patient.user.full_name

class CreateAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["patient","doctor","hospital","appointment_date","time_slot","visit_type","chief_complaint","fee"]

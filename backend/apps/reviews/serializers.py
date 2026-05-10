from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    class Meta:
        model = Review
        fields = "__all__"
    def get_patient_name(self, obj):
        return obj.patient.user.full_name

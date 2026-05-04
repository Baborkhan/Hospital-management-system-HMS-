from rest_framework import serializers
from .models import Campaign

class CampaignSerializer(serializers.ModelSerializer):
    hospital_name = serializers.SerializerMethodField()
    ctr = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = ["id", "hospital", "hospital_name", "campaign_type", "title", "description",
                  "budget", "start_date", "end_date", "is_active", "impressions", "clicks", "ctr", "created_at"]
        read_only_fields = ["id", "impressions", "clicks", "created_at"]

    def get_hospital_name(self, obj):
        return obj.hospital.name

    def get_ctr(self, obj):
        return round(obj.clicks / obj.impressions * 100, 2) if obj.impressions else 0.0

    def validate(self, data):
        if data.get("start_date") and data.get("end_date"):
            if data["end_date"] <= data["start_date"]:
                raise serializers.ValidationError("End date must be after start date.")
        return data

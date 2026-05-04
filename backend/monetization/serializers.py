from rest_framework import serializers
from .models import Subscription

class SubscriptionSerializer(serializers.ModelSerializer):
    hospital_name = serializers.SerializerMethodField()
    is_expired = serializers.SerializerMethodField()
    days_remaining = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ["id", "hospital", "hospital_name", "plan", "start_date", "end_date",
                  "amount", "is_active", "is_expired", "days_remaining"]
        read_only_fields = ["id"]

    def get_hospital_name(self, obj):
        return obj.hospital.name

    def get_is_expired(self, obj):
        from django.utils import timezone
        return obj.end_date < timezone.now().date()

    def get_days_remaining(self, obj):
        from django.utils import timezone
        delta = obj.end_date - timezone.now().date()
        return max(delta.days, 0)

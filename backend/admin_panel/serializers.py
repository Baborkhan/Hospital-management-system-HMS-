from rest_framework import serializers

class DashboardSummarySerializer(serializers.Serializer):
    total_hospitals = serializers.IntegerField()
    total_doctors = serializers.IntegerField()
    total_patients = serializers.IntegerField()
    today_appointments = serializers.IntegerField()
    pending_appointments = serializers.IntegerField()
    beds_free = serializers.IntegerField()
    icu_free = serializers.IntegerField()
    monthly_revenue = serializers.FloatField()
    weekly_chart = serializers.ListField()

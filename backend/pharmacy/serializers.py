from rest_framework import serializers
from .models import Medicine, PharmacyOrder, PharmacyOrderItem

class MedicineSerializer(serializers.ModelSerializer):
    stock_status = serializers.ReadOnlyField()
    class Meta:
        model = Medicine
        fields = "__all__"

class OrderItemSerializer(serializers.ModelSerializer):
    medicine_name = serializers.SerializerMethodField()
    class Meta:
        model = PharmacyOrderItem
        fields = "__all__"
    def get_medicine_name(self, obj):
        return obj.medicine.name

class PharmacyOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = PharmacyOrder
        fields = "__all__"

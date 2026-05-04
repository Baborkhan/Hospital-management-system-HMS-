from rest_framework import serializers
from .models import LoyaltyTransaction

class LoyaltyTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyTransaction
        fields = ["id", "transaction_type", "points", "description", "balance_after", "created_at"]
        read_only_fields = ["id", "balance_after", "created_at"]

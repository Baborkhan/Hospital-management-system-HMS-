from rest_framework import serializers
from apps.accounts.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "full_name", "phone", "role", "is_verified",
                  "date_joined", "loyalty_points"]
        read_only_fields = ["id", "email", "role", "date_joined"]

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["full_name", "phone"]

    def validate_full_name(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Full name must be at least 3 characters.")
        return value.strip()

    def validate_phone(self, value):
        import re
        phone = re.sub(r'[\s\-\(\)]', '', value)
        if not re.match(r'^(\+880|880|0)[0-9]{9,10}$', phone):
            raise serializers.ValidationError("Enter a valid Bangladeshi phone number.")
        return phone

from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["email", "full_name", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  # Foydalanuvchini yaratish
        refresh = RefreshToken.for_user(user)  # JWT token generatsiya qilish

        return {
            "user": {
                "email": user.email,
                "full_name": user.full_name,
            },
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

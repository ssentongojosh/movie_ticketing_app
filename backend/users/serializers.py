# users/serializers.py

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.db import transaction # Import transaction for atomic operations
from .models import CustomUser
from userprofile.models import UserProfile


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        # Use email as the primary registration field as per your ERD
        fields = ('email', 'password', 'password2', 'phone_number') # 'user_type' is not on your ERD
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'phone_number': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        # Check if email is unique (ModelSerializer does this by default if unique=True)
        # Check if phone_number is unique
        return attrs

    @transaction.atomic # Ensures that if anything fails, the entire operation is rolled back
    def create(self, validated_data):
        validated_data.pop('password2')
        # We use a custom create_user method in our CustomUserManager
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data['phone_number']
            # We can set other fields here if needed
        )
        # Note: The Profile for this user is automatically created by our signal
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('full_name', 'location_preferences', 'notification_preferences', 'is_active', 'payment_methods')
        read_only_fields = ('is_active', 'created_at', 'updated_at')

class UserProfileSerializer(serializers.ModelSerializer):
    # Nested serializer to include the profile data
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'id', 'email', 'phone_number', 'provider', 'provider_id', 'is_verified',
            'status', 'is_admin', 'is_anonymous', 'date_joined', 'last_login',
            'profile'
        )
        read_only_fields = (
            'id', 'email', 'is_verified', 'status', 'is_admin', 'is_anonymous',
            'date_joined', 'last_login', 'provider', 'provider_id'
        )

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('full_name', 'location_preferences', 'notification_preferences', 'payment_methods')
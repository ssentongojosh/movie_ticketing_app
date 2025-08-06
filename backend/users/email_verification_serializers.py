
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils import timezone
from django.core.exceptions import ValidationError

User = get_user_model()

class EmailVerificationRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
            if user.is_verified:
                raise serializers.ValidationError("This email address is already verified.")
            self.user = user
        except User.DoesNotExist:
            # For security, return a generic message if user doesn't exist
            raise serializers.ValidationError("No active user is associated with this email address.")
        return value

    def save(self):
        # Send the verification email using the method on CustomUser
        
        print(f"Sending verification email to: {self.user.email}") 
        
        request = self.context.get('request')
        self.user.send_verification_email(request)


class EmailVerificationConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    def validate(self, attrs):
        try:
            uid = force_str(urlsafe_base64_decode(attrs['uid']))
            user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({"uid": "Invalid user ID."})

        if not default_token_generator.check_token(user, attrs['token']):
            raise serializers.ValidationError({"token": "Invalid or expired token."})

        if user.is_verified:
            raise serializers.ValidationError({"email": "This email is already verified."})

        self.user = user
        return attrs

    def save(self):
        # Mark user as verified and set timestamp
        self.user.is_verified = True
        self.user.email_verified_at = timezone.now()
        self.user.save(update_fields=['is_verified', 'email_verified_at'])
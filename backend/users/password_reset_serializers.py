# users/password_reset_serializers.py

from rest_framework import serializers
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.conf import settings
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .models import CustomUser as User

User = get_user_model()

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def get_email_options(self, user, uid, token):
        """
        Returns a dictionary of options for the password reset email.
        This can be customized to include specific templates, subject, etc.
        """
        return {
            'email_template_name': 'password_reset/password_reset_email.html',
            'subject_template_name': 'password_reset/password_reset_subject.txt',
            'html_email_template_name': None, # Can specify an HTML template
            'extra_email_context': {
                'password_reset_confirm_url':settings.PASSWORD_RESET_CONFIRM_URL.format(uid=uid,token=token) ,
                'user': user,
                'uid': uid,
                'token': token,
            },
        }

    def validate_email(self, value):
        # Ensure the email exists in our system
        if not User.objects.filter(email=value, is_active=True).exists():
            # For security, it's often better to return a generic message
            # rather than confirming if an email exists or not.
            raise serializers.ValidationError("No active user is associated with this email address.")
        return value

    def save(self, **kwargs):
        # This method is called by the view to send the email
        request = self.context.get('request')
        
        if not request:
            raise serializers.ValidationError("Request context is required")
    
        
        email = self.validated_data['email']
        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError("No active user is associated with this email address.")

        # Manually generate uid and token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        
        # Use Django's built-in PasswordResetForm to handle sending the email
        form = PasswordResetForm({'email': email})
        if form.is_valid():
            # Pass the request object and email options to the form's save method
            form.save(
                domain_override=request.get_host(), # Use current host for domain in email link
                use_https=request.is_secure(), # Use HTTPS if request is secure
                request=request,
                from_email=settings.DEFAULT_FROM_EMAIL,
                **self.get_email_options(user,uid,token)
            )
        else:
            # This should ideally not happen if validate_email is robust
            raise serializers.ValidationError(form.errors)


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    new_password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})

        # Decode UID and validate token
        try:
            uid = force_str(urlsafe_base64_decode(attrs['uid']))
            user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({"uid": "Invalid user ID."})

        if not default_token_generator.check_token(user, attrs['token']):
            raise serializers.ValidationError({"token": "Invalid or expired token."})

        self.user = user # Store user for later use in save()
        return attrs

    def save(self):
        # This method is called by the view to set the new password
        user = self.user
        new_password = self.validated_data['new_password']
        
        # Use Django's built-in SetPasswordForm to handle setting the password
        form = SetPasswordForm(user, {'new_password1': new_password, 'new_password2': new_password})
        if form.is_valid():
            form.save()
        else:
            # This should ideally not happen if validate is robust
            raise serializers.ValidationError(form.errors)
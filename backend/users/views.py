from django.shortcuts import render

# Create your views here.
# users/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .password_reset_serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from .email_verification_serializers import EmailVerificationRequestSerializer,EmailVerificationConfirmSerializer




from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
    ProfileUpdateSerializer,
)
from .models import CustomUser

class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            email_request_serializer = EmailVerificationRequestSerializer(
                data={'email': user.email},
                context={'request': request} # Pass the original request to the serializer
            )
            if email_request_serializer.is_valid():
                email_request_serializer.save()
            else:
                # Log this error, but don't fail the registration if email sending fails
                print(f"Error sending verification email for {user.email}: {email_request_serializer.errors}")
            # --- END NEW ---

            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "User registered successfully. Please check your email to verify your account.",
                    "user": UserProfileSerializer(user).data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    pass


class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # The profile is accessed via the one-to-one relationship
        profile = request.user.profile
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        # We need to handle updates to both the CustomUser and Profile models
        user_serializer = UserProfileSerializer(
            request.user, data=request.data, partial=True
        )
        profile_serializer = ProfileUpdateSerializer(
            request.user.profile, data=request.data, partial=True
        )

        if user_serializer.is_valid() and profile_serializer.is_valid():
            user_serializer.save()
            profile_serializer.save()
            return Response(
                UserProfileSerializer(request.user).data, status=status.HTTP_200_OK
            )

        errors = {}
        if not user_serializer.is_valid():
            errors.update(user_serializer.errors)
        if not profile_serializer.is_valid():
            errors.update(profile_serializer.errors)

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PasswordResetRequestAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Password reset email has been sent if an active user with that email exists."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Password has been reset successfully."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class EmailVerificationRequestAPIView(APIView):
    permission_classes = [AllowAny] # Allow unverified users to request verification

    def post(self, request):
        serializer = EmailVerificationRequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Email verification link has been sent if the email is unverified."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmailVerificationConfirmAPIView(APIView):
    permission_classes = [AllowAny] # Allow unauthenticated access for verification

    def post(self, request):
        serializer = EmailVerificationConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Email has been successfully verified."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

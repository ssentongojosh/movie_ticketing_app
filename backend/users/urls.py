# users/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserRegistrationAPIView, CustomTokenObtainPairView, UserProfileAPIView,PasswordResetRequestAPIView,PasswordResetConfirmAPIView,EmailVerificationRequestAPIView,EmailVerificationConfirmAPIView 

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile', UserProfileAPIView.as_view(), name='user_profile'),
    path('password-reset/request/', PasswordResetRequestAPIView.as_view(), name='password_reset_request'),
    path('password-reset/confirm/', PasswordResetConfirmAPIView.as_view(), name='password_reset_confirm'),
    path('email-verification/request/', EmailVerificationRequestAPIView.as_view(), name='email_verification_request'),
    path('email-verification/confirm/', EmailVerificationConfirmAPIView.as_view(), name='email_verification_confirm'),
]
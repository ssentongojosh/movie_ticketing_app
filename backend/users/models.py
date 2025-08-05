from django.db import models

# Create your models here.
# users/models.py

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
import uuid # For UUID primary keys

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password) # Handles password hashing
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True) # Match your ERD
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('email_verified_at', timezone.now())

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True) # Assuming unique
    # password_hash - Handled by AbstractBaseUser's password field and set_password method
    provider = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., 'email', 'google', 'facebook'")
    provider_id = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    status = models.CharField(max_length=50, default='active', help_text="e.g., 'active', 'inactive', 'suspended'") # Can be an Enum later
    confirmation_sent_at = models.DateTimeField(null=True, blank=True)
    confirmation_expires_at = models.DateTimeField(null=True, blank=True)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    is_admin = models.BooleanField(default=False) # Maps to your ERD, could be mapped to is_staff/is_superuser

    password_reset_token = models.CharField(max_length=255, blank=True, null=True)
    token_expires_at = models.DateTimeField(null=True, blank=True)

    # Django's built-in user fields often used in admin/authentication:
    is_staff = models.BooleanField(default=False, help_text="Designates whether the user can log into this admin site.")
    is_superuser = models.BooleanField(default=False, help_text="Designates that this user has all permissions without explicitly assigning them.")
    is_active = models.BooleanField(default=True, help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.")
    date_joined = models.DateTimeField(default=timezone.now) # Equivalent to created_at
    last_login = models.DateTimeField(null=True, blank=True) # Equivalent to updated_at for login time

    # Our custom user manager
    objects = CustomUserManager()

    USERNAME_FIELD = 'email' # Use email for authentication
    REQUIRED_FIELDS = ['phone_number'] # Fields required for createsuperuser besides USERNAME_FIELD and password

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined'] # Order by newest first
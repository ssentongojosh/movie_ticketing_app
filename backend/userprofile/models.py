from django.db import models

# Create your models here.
# userprofile/models.py


import uuid
from users.models import CustomUser # Import our CustomUser model

class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='userprofile' # Access profile from user via user.userprofile
    )
    full_name = models.CharField(max_length=255, blank=True, null=True)
    location_preferences = models.CharField(max_length=255, blank=True, null=True)
    notification_preferences = models.JSONField(default=dict, blank=True, null=True) # Django's JSONField
    is_active = models.BooleanField(default=True, help_text='active account or deactivated')
    payment_methods = models.JSONField(default=list, blank=True, null=True) # Storing list of payment methods

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.email}"

    # Signal to create/update profile when user is created/updated
    
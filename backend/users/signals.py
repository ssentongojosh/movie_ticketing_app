# users/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from userprofile.models import UserProfile

@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    # Optional: If you want to handle updates to the user that affect profile
    # instance.userprofile.save() # This would be called if profile attributes directly depended on user fields
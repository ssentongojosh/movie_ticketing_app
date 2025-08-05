# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from userprofile.models import UserProfile # Import Profile model for inline display
# Inline for Profile to show it directly on the User admin page
class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

    # --- IMPORTANT CHANGES HERE ---
    # Replace 'username' with 'email' in list_display
    list_display = ('email', 'phone_number', 'is_staff', 'is_active', 'is_admin', 'is_verified', 'date_joined')
    # Replace 'username' with 'email' in search_fields
    search_fields = ('email', 'phone_number', 'profile__full_name') # Added profile__full_name for searching
    list_filter = ('is_staff', 'is_active', 'is_admin', 'is_verified', 'date_joined')

    # Define the fieldsets for adding/changing a user in the admin
    fieldsets = (
        (None, {'fields': ('email', 'password')}), # Use 'email' instead of 'username'
        ('Personal info', {'fields': ('phone_number', 'is_verified', 'email_verified_at', 'status', 'provider', 'provider_id')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'confirmation_sent_at', 'confirmation_expires_at', 'password_reset_token', 'token_expires_at')}),
        ('Other', {'fields': ('is_anonymous',)}),
    )
    # Define the fields to be added when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password', 'password2', 'is_admin', 'is_staff', 'is_superuser', 'is_active', 'is_verified'),
        }),
    )
    # Ensure password2 is handled for new user creation
    add_form_template = 'admin/auth/user/add_form.html'

    # --- FIX THE ORDERING ERROR HERE ---
    # Change 'username' to a valid field like 'email' or 'date_joined'
    ordering = ('email',) # Or ('date_joined',) if you prefer to order by creation date

# Register our CustomUser model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)

# Register Profile model (already done, just for completeness)
@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'is_active', 'created_at', 'updated_at')
    search_fields = ('user__email', 'full_name', 'location_preferences')
    list_filter = ('is_active', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
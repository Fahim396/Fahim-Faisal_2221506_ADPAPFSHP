from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for the extended User model."""

    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'created_at')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Extended Info', {
            'fields': ('role', 'phone', 'location', 'profile_image'),
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Extended Info', {
            'fields': ('role', 'email', 'first_name', 'last_name', 'phone', 'location'),
        }),
    )

"""
Module for admin page for custom User and Role models.

This module provides ModelAdmin classes for the Role and CustomUser models
for customizing their apperance and behaviour in the Django admin site.

The 'RoleAdmin' class is a ModelAdmin class for Role model.
The 'CustomUserAdmin' class is a ModelAdmin class blased on the built-in UserAdmin class.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Role, CustomUser
from .forms import CustomUserChangeForm, CustomUserCreationForm


class RoleAdmin(admin.ModelAdmin):
    """
    ModelAdmin for Role model.

    Definition how Role instances are displayed and edited in admin site.
    It sets which fields are displayed and available.
    """

    list_display = ["name", "thumbnail_size", "allow_original", "allow_expiring"]


class CustomUserAdmin(UserAdmin):
    """ "
    ModelAdmin for the CustomUser model.

    Class based on the built-in UserAdmin class.
    Definition how CustomUser instances are displayed and edited in the Django admin site.
    """

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("username", "is_active", "role", "is_superuser")
    fieldsets = (
        (None, {"fields": ("username", "password", "is_active", "is_superuser")}),
        ("Permissions", {"fields": ("role",)}),
    )
    filter_horizontal = ()


admin.site.register(Role, RoleAdmin)
admin.site.register(CustomUser, CustomUserAdmin)

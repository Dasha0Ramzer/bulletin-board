from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "first_name", "last_name", "role", "is_staff")

    search_fields = ("email", "first_name", "last_name")

    fieldsets = BaseUserAdmin.fieldsets + (("Дополнительная информация", {"fields": ("phone", "role", "image")}),)

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Дополнительная информация", {"fields": ("phone", "role", "image")}),
    )

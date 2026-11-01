from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Поля, которые будут отображаться в списке пользователей
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff')

    # Поля, по которым можно искать
    search_fields = ('email', 'first_name', 'last_name')

    # Настройка формы редактирования (добавляем наши кастомные поля)
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('phone', 'role', 'image')}),
    )

    # Настройка формы создания пользователя (если создаешь через админку)
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Дополнительная информация', {'fields': ('phone', 'role', 'image')}),
    )
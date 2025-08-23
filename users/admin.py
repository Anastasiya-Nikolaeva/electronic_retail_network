from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    """
    Админ-панель для управления пользователями.
    """

    list_display = ("email", "username", "is_active", "is_staff")
    search_fields = ("email", "username")
    list_filter = ("is_active", "is_staff")


# Регистрация модели CustomUser в админке
admin.site.register(CustomUser, CustomUserAdmin)

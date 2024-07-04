from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "last_name", "first_name", "email", "is_staff", "is_active")
    search_fields = ("username", "last_name", "first_name", "email")
    list_filter = ("is_staff", "is_active")

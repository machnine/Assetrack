""" Custom user model for the application. """
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CustomUser(AbstractUser):
    """Custom user model for the application."""

    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name="customuser_groups",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name="customuser_user_permissions",
        related_query_name="customuser",
    )

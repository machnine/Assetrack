"""various associated models"""

from django.conf import settings
from django.db import models

USER = settings.AUTH_USER_MODEL


class Status(models.Model):
    """status of the asset"""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Calibration(models.Model):
    """Type of calibration required"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class EquipmentType(models.Model):
    """type of equipment e.g. centrifuge, microscope etc."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "equipment types"
        ordering = ["name"]

class Category(models.Model):
    """category of the asset"""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]


class Location(models.Model):
    """location of the asset"""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "locations"
        ordering = ["name"]

class Company(models.Model):
    """associated company of the asset"""

    name = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "companies"
        ordering = ["name"]
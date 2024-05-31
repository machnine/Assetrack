"""This module contains the model for the asset records"""

from django.conf import settings
from django.db import models

USER = settings.AUTH_USER_MODEL


class AbstractRecord(models.Model):
    """Abstract record for repair and maintenance records of the asset"""

    date = models.DateField()
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.date} - {self.name}"


class EquipmentRecord(AbstractRecord):
    """Record for the equipment"""

    equipment = models.ForeignKey("Equipment", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Equipment Record"
        verbose_name_plural = "Equipment Records"

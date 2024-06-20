"""This module contains the model for the asset records"""

from django.conf import settings
from django.db import models

from attachment.models import Attachment

USER = settings.AUTH_USER_MODEL


class AbstractRecord(models.Model):
    """Abstract record for repair and maintenance records of the asset"""

    date = models.DateField()
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, blank=True, related_name="+")

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.date} - {self.description[:50]}"


# equipment record models
class EquipmentRecord(AbstractRecord):
    """Record for the equipment"""

    record_type = models.ForeignKey("RecordType", on_delete=models.CASCADE)
    equipment = models.ForeignKey("Equipment", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Equipment Record"
        verbose_name_plural = "Equipment Records"
        ordering = ["-date"]

    def has_attachment(self):
        """Check if the record has an attachment"""
        if EquipmentRecordAttachment.objects.filter(object_id=self.id).exists():
            return True
        return False


class EquipmentRecordAttachment(Attachment):
    """Attachment for the equipment record"""

    uploaded_by = models.ForeignKey(
        USER, on_delete=models.SET_NULL, null=True, blank=True, related_name="equipment_record_attachments"
    )


class RecordType(models.Model):
    """Model for record type"""

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


# software record model
class SoftwareRecord(AbstractRecord):
    """Record for the software"""

    software = models.ForeignKey("Software", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Software Record"
        verbose_name_plural = "Software Records"
        ordering = ["-date"]

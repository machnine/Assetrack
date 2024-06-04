"""equipment model"""

from django.conf import settings
from django.db import models

from attachment.models import Attachment

USER = settings.AUTH_USER_MODEL


class Equipment(models.Model):
    """Equipment model"""

    name = models.CharField(max_length=100)
    manufacturer = models.ForeignKey("Company", on_delete=models.PROTECT, related_name="manufacturer")
    model_number = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    inventory_number = models.CharField(max_length=100, null=True, blank=True)
    porcurement_date = models.DateField(null=True, blank=True)
    commission_date = models.DateField(null=True, blank=True)
    warranty_end = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    category = models.ForeignKey("Category", on_delete=models.PROTECT)
    location = models.ForeignKey("Location", on_delete=models.PROTECT)
    status = models.ForeignKey("Status", on_delete=models.PROTECT)
    service_provider = models.ForeignKey(
        "Company", on_delete=models.PROTECT, related_name="service_provider", blank=True, null=True
    )

    def __str__(self):
        return self.name

    def has_attachment(self):
        """Check if the equipment has an attachment"""
        if EquipmentAttachment.objects.filter(object_id=self.id).exists():
            return True
        return False

    class Meta:
        ordering = ["name"]


class EquipmentAttachment(Attachment):
    """Attachment model for equipment"""

    uploaded_by = models.ForeignKey(
        USER, on_delete=models.SET_NULL, null=True, blank=True, related_name="equipment_attachments"
    )

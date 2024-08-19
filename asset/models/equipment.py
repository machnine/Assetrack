"""equipment model"""

from django.conf import settings
from django.db import models

from attachment.models import Attachment

from .record import EquipmentRecord

USER = settings.AUTH_USER_MODEL


class Equipment(models.Model):
    """Equipment model"""

    name = models.CharField(max_length=100, unique=True)
    manufacturer = models.ForeignKey("Company", on_delete=models.PROTECT, related_name="manufacturer")
    model_number = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    inventory_number = models.CharField(max_length=100, null=True, blank=True, unique=True)
    received_date = models.DateField(null=True, blank=True)
    commission_date = models.DateField(null=True, blank=True)
    warranty_end = models.DateField(null=True, blank=True)
    replacement_date = models.DateField(null=True, blank=True)
    value = models.IntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    category = models.ForeignKey("Category", on_delete=models.PROTECT)
    equipment_type = models.ForeignKey("EquipmentType", on_delete=models.PROTECT)
    location = models.ForeignKey("Location", on_delete=models.PROTECT)
    status = models.ForeignKey("Status", on_delete=models.PROTECT)
    calibration = models.ForeignKey("Calibration", on_delete=models.PROTECT, null=True, blank=True)
    service_provider = models.ForeignKey(
        "Company", on_delete=models.PROTECT, related_name="service_provider", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, blank=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, blank=True, related_name="+")

    def __str__(self):
        return self.name

    def has_attachment(self):
        """Check if the equipment has an attachment"""
        if EquipmentAttachment.objects.filter(object_id=self.id).exists():
            return True
        return False

    def last_serviced(self):
        """Return the last service date"""
        records = EquipmentRecord.objects.filter(
            models.Q(equipment=self) & models.Q(record_type__name="Service")
        ).order_by("-date")
        if records.exists():
            return records[0].date

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["equipment_type", "status"]),
            models.Index(fields=["equipment_type"]),
            models.Index(fields=["status"]),
        ]


class EquipmentAttachment(Attachment):
    """Attachment model for equipment"""

    uploaded_by = models.ForeignKey(
        USER, on_delete=models.SET_NULL, null=True, blank=True, related_name="equipment_attachments"
    )

    class Meta:
        ordering = ["-uploaded_at"]

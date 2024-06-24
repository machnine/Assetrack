"""models for software"""

from django.conf import settings
from django.db import models

from attachment.models import Attachment

USER = settings.AUTH_USER_MODEL


class License(models.Model):
    """License model"""

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class SoftwareType(models.Model):
    """Software type model"""

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Software(models.Model):
    """Software model"""

    name = models.CharField(max_length=50, unique=True)
    version = models.CharField(max_length=50)
    license_type = models.ForeignKey(License, on_delete=models.CASCADE)
    software_type = models.ForeignKey(SoftwareType, on_delete=models.CASCADE)
    website = models.URLField(blank=True, null=True)
    implemented_date = models.DateField(blank=True, null=True)
    decommission_date = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    source_code = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    last_updated_at = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, blank=True, related_name="+")

    def __str__(self):
        return f"{self.name} {self.version}"


class SoftwareAttachment(Attachment):
    """Attachment model for software"""

    uploaded_by = models.ForeignKey(
        USER, on_delete=models.SET_NULL, null=True, blank=True, related_name="software_attachments"
    )

    class Meta:
        ordering = ["-uploaded_at"]

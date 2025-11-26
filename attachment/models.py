"""Attachment models"""

from pathlib import Path

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.deconstruct import deconstructible

USER = settings.AUTH_USER_MODEL


@deconstructible
class UploadToPathAndRename:
    """Callable class to upload files to a path and rename them"""

    def __init__(self, path):
        self.sub_path = Path(path)

    def __call__(self, instance, filename):
        # Construct a safe file name
        new_filename = Path(filename).name

        # Using the ContentType framework to get the related object's ID
        object_id = getattr(instance, "object_id", None)

        if object_id:
            # Define the folder name based on the instance's class to avoid collision
            folder_name = instance._meta.model_name.replace("attachment", "")
            sub_folder = str(object_id)
        else:
            # Define the folder name for generic attachments
            folder_name = "documents"
            sub_folder = ""

        # Construct the new path and filename
        return str(self.sub_path / folder_name / sub_folder / new_filename)


class AttachmentBase(models.Model):
    """Attachment base model"""

    file = models.FileField("file", upload_to=UploadToPathAndRename("attachments"))
    uploaded_at = models.DateTimeField("uploaded at", auto_now_add=True)
    uploaded_by = models.ForeignKey(
        USER, on_delete=models.SET_NULL, null=True, blank=True, related_name="uploaded_attachments"
    )
    name = models.CharField("name", max_length=255, blank=True)
    description = models.TextField("description", blank=True)

    class Meta:
        """Meta options"""

        abstract = True
        verbose_name = "attachment"
        verbose_name_plural = "attachments"

    @property
    def filename(self):
        """Return filename"""
        return Path(self.file.name).name

    @property
    def filetype(self):
        """Return filetype"""
        if suffix := Path(self.file.name).suffix:
            return suffix[1:].lower()

    @property
    def file_exists(self):
        """Check if the file exists on disk"""
        try:
            return self.file and self.file.storage.exists(self.file.name)
        except Exception:
            return False

    @property
    def file_size(self):
        """Return file size safely, or None if file is missing"""
        try:
            if self.file_exists:
                return self.file.size
        except Exception:
            pass
        return None

    def get_verbose_name(self, plural=False):
        return self._meta.verbose_name_plural if plural else self._meta.verbose_name

    def __str__(self):
        """String representation"""
        return self.name or f"Attachment: {Path(self.file.name).name}"


class Attachment(AttachmentBase):
    """Attachment abstract model"""

    # GenericForeignKey setup
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta(AttachmentBase.Meta):
        """Meta options"""

        abstract = True


class Document(AttachmentBase):
    """Generic attachment model with no relation to any object"""

    class Meta(AttachmentBase.Meta):
        """Meta options"""

        ordering = ["-uploaded_at"]  # Newest first

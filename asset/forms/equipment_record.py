"""equipment record form module."""

from django import forms

from asset.models import EquipmentRecord, EquipmentRecordAttachment
from attachment.forms import AttachmentForm


class EquipmentRecordForm(forms.ModelForm):
    """EquipmentRecord form class"""

    class Meta:
        model = EquipmentRecord
        fields = ["date", "record_type", "description"]


class EquipmentRecordAttachmentUploadForm(AttachmentForm):
    """Form for uploading an attachment for equipment."""

    class Meta(AttachmentForm.Meta):
        model = EquipmentRecordAttachment
        fields = ["file", "name", "description"]


class EquipmentRecordAttachmentUpdateForm(AttachmentForm):
    """Form for updating an attachment for equipment."""

    class Meta(AttachmentForm.Meta):
        model = EquipmentRecordAttachment
        exclude = ["file"]

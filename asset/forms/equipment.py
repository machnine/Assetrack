"""equipment form module."""

from django import forms

from asset.models import Equipment, EquipmentAttachment
from attachment.forms import AttachmentForm


class EquipmentForm(forms.ModelForm):
    """Equipment form class"""

    class Meta:
        model = Equipment
        fields = "__all__"


class EquipmentAttachmentUploadForm(AttachmentForm):
    """Form for uploading an attachment for equipment."""

    class Meta(AttachmentForm.Meta):
        model = EquipmentAttachment
        fields = ["file", "name", "description"]


class EquipmentAttachmentUpdateForm(AttachmentForm):
    """Form for updating an attachment for equipment."""

    class Meta(AttachmentForm.Meta):
        model = EquipmentAttachment
        exclude = ["file"]

"""equipment record form module."""

from django import forms

from asset.models import EquipmentRecord, EquipmentRecordAttachment
from attachment.forms import AttachmentForm


class EquipmentRecordForm(forms.ModelForm):
    """EquipmentRecord form class"""

    class Meta:
        model = EquipmentRecord
        fields = ["date", "record_type", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"].widget = forms.DateInput(attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d")
        self.fields["record_type"].widget.attrs.update({"class": "form-control"})
        self.fields["description"].widget.attrs.update({"rows": 3, "class": "form-control"})


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

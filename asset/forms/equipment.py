"""equipment form module."""

from django import forms

from asset.models import Equipment, EquipmentAttachment
from attachment.forms import AttachmentForm


class EquipmentForm(forms.ModelForm):
    """Equipment form class"""

    class Meta:
        model = Equipment
        fields = [
            "name",
            "manufacturer",
            "model_number",
            "serial_number",
            "inventory_number",
            "received_date",
            "commission_date",
            "warranty_end",
            "replacement_date",
            "value",
            "notes",
            "category",
            "equipment_type",
            "location",
            "status",
            "calibration",
            "service_provider",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # all fields css class
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})
        # Date fields
        date_fields = ["received_date", "commission_date", "warranty_end", "replacement_date"]
        for date_field in date_fields:
            self.fields[date_field].widget = forms.DateInput(
                attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d"
            )
        # other fields
        self.fields["name"].widget.attrs.update({"autofocus": True})
        self.fields["notes"].widget.attrs.update({"rows": 3})


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

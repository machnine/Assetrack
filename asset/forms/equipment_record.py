"""equipment record form module."""

from django import forms
from django.utils import timezone

from asset.models import Category, Equipment, EquipmentRecord, EquipmentRecordAttachment, RecordType
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

    def clean_date(self):
        """Ensure the date is not in the future."""
        date = self.cleaned_data["date"]

        if date:
            if date > timezone.now().date():
                raise forms.ValidationError("The date cannot be in the future.")

        return date


class EquipmentRecordTimelineFilterForm(forms.Form):
    """Filters for the equipment record timeline."""

    start_date = forms.DateField(
        label="From",
        required=False,
        widget=forms.DateInput(
            attrs={"type": "date", "class": "form-control form-control-sm"},
            format="%Y-%m-%d",
        ),
    )
    end_date = forms.DateField(
        label="To",
        required=False,
        widget=forms.DateInput(
            attrs={"type": "date", "class": "form-control form-control-sm"},
            format="%Y-%m-%d",
        ),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All categories",
        widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
    )
    equipment = forms.ModelChoiceField(
        queryset=Equipment.objects.all(),
        required=False,
        empty_label="All equipment",
        widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
    )
    record_type = forms.ModelChoiceField(
        queryset=RecordType.objects.all(),
        required=False,
        empty_label="All record types",
        widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("The from date must be on or before the to date.")
        return cleaned_data


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

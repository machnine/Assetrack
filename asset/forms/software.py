"""This module contains the forms for the software app."""

from django import forms

from asset.models import Software, SoftwareAttachment
from attachment.forms import AttachmentForm


class SoftwareForm(forms.ModelForm):
    """Software form"""

    class Meta:
        model = Software
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
        self.fields["description"].widget.attrs.update({"rows": 3})
        self.fields["active"].widget.attrs.update({"class": "form-check-input"}, default=True)


class SoftwareAttachmentUploadForm(AttachmentForm):
    """Form for uploading an attachment for Software."""

    class Meta(AttachmentForm.Meta):
        model = SoftwareAttachment
        fields = ["file", "name", "description"]


class SoftwareAttachmentUpdateForm(AttachmentForm):
    """Form for updating an attachment for Software."""

    class Meta(AttachmentForm.Meta):
        model = SoftwareAttachment
        exclude = ["file"]

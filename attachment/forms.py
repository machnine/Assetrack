"""Attachment forms."""

from pathlib import Path

from django import forms

from .models import Attachment

ALLOWED_FILE_TYPES = (".jpg", ".jpeg", ".png", ".bmp", ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".csv", ".txt", ".xml")
MAX_FILE_SIZE = 2 ** 20 * 10  # 10MB in bytes (2 ** 10 = 1KB, 2 ** 20 = 1MB)

class AttachmentForm(forms.ModelForm):
    """Form for uploading an attachment"""

    class Meta:
        model = Attachment
        fields = ("file", "name", "description")

    def clean_file(self):
        """Ensure the uploaded file type is allowed."""
        file = self.cleaned_data.get("file")
        file_type = Path(file.name).suffix.lower()

        # Check the file type
        if file_type not in ALLOWED_FILE_TYPES:
            raise forms.ValidationError(f"Unsupported file extension {file_type}")
        
        # Check the file size
        if file.size > MAX_FILE_SIZE:
            raise forms.ValidationError(f"File size exceeds the maximum of {MAX_FILE_SIZE / 2 ** 20} MB")
        return file

    def clean(self):
        """If no name is provided, use the file's name without the extension."""
        cleaned_data = super().clean()
        file = cleaned_data.get("file")
        name = cleaned_data.get("name")

        # If no name is provided, use the file's name without the extension
        if file and not name:
            name = Path(file.name).stem
            cleaned_data["name"] = name

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"class": "form-control"})
        self.fields["description"].widget.attrs.update({"class": "form-control", "rows": 2})

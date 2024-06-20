"""software record form module."""

from django import forms

from asset.models import SoftwareRecord


class SoftwareRecordForm(forms.ModelForm):
    """SoftwareRecord form class"""

    class Meta:
        model = SoftwareRecord
        fields = ["date", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"].widget = forms.DateInput(attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d")
        self.fields["description"].widget.attrs.update({"rows": 3, "class": "form-control"})

"""forms for maintenance records"""

from django import forms

from asset.models import MaintenanceRecord, MaintenanceTask


class MaintenanceTaskForm(forms.ModelForm):
    """Maintenance task form"""

    class Meta:
        model = MaintenanceTask
        fields = ["name", "equipment_type", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
        self.fields["description"].widget.attrs.update({"rows": 3})


class MaintenanceRecordForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRecord
        fields = ["date", "equipment", "comments"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
            self.fields["date"].widget = forms.DateInput(
                attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d"
            )
            self.fields["comments"].widget.attrs.update({"rows": 3})

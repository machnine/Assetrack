"""forms for maintenance records"""

from django import forms

from asset.models import MaintenanceRecord, MaintenanceTask


class MaintenanceTaskForm(forms.ModelForm):
    """Maintenance task form"""

    class Meta:
        model = MaintenanceTask
        fields = ["name", "equipment_type", "color", "description"]
        widgets = {
            "color": forms.TextInput(attrs={"type": "color", "class": "form-control form-control-color"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ["name", "equipment_type", "description"]:
            self.fields[field].widget.attrs.update({"class": "form-control"})
        self.fields["description"].widget.attrs.update({"rows": 3})


class MaintenanceRecordForm(forms.ModelForm):
    tasks = forms.ModelMultipleChoiceField(
        queryset=MaintenanceTask.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        model = MaintenanceRecord
        fields = ["date", "equipment", "tasks", "comments"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["date"].widget = forms.DateInput(attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d")
        self.fields["equipment"].widget.attrs.update({"class": "form-control"})
        self.fields["comments"].widget.attrs.update({"class": "form-control", "rows": 3})

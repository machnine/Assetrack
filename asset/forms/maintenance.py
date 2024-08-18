"""forms for maintenance records"""

from django import forms

from asset.models import MaintenanceRecord, MaintenanceTask


# class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
#     def get_context(self, name, value, attrs):
#         context = super().get_context(name, value, attrs)
#         for choice in context["widget"]["optgroups"]:
#             for subwidget in choice[1]:
#                 subwidget["attrs"]["class"] = "form-check-input"
#         return context


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

        # # Dynamically set the queryset for the tasks field based on the equipment type
        # if self.instance.pk and self.instance.equipment:
        #     equipment_type = self.instance.equipment.equipment_type
        #     self.fields["tasks"].queryset = MaintenanceTask.objects.filter(equipment_type=equipment_type)
        #     self.fields["tasks"].initial = self.instance.maintenance.values_list("task", flat=True)
        # else:
        #     self.fields["tasks"].queryset = MaintenanceTask.objects.all()

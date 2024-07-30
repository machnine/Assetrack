"""forms for asset app"""

from django import forms

from asset.models import Category, Company, EquipmentType, Location, Schedule, Status


class CompanyForm(forms.ModelForm):
    """Company form"""

    class Meta:
        model = Company
        fields = ["name", "phone", "email", "website", "notes"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
        self.fields["notes"].widget.attrs.update({"rows": 3})


class CategoryForm(forms.ModelForm):
    """Category form"""

    class Meta:
        model = Category
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
        self.fields["description"].widget.attrs.update({"rows": 3})


class LocationForm(forms.ModelForm):
    """Location form"""

    class Meta:
        model = Location
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
        self.fields["description"].widget.attrs.update({"rows": 3})


class StatusForm(forms.ModelForm):
    """Status form"""

    class Meta:
        model = Status
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
        self.fields["description"].widget.attrs.update({"rows": 3})


class EquipmentTypeForm(forms.ModelForm):
    """EquipmentType Form"""

    class Meta:
        model = EquipmentType
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
        self.fields["description"].widget.attrs.update({"rows": 3})


class ScheduleForm(forms.ModelForm):
    """Asset Schedule Form"""

    class Meta:
        model = Schedule
        fields = ["schedule_date", "status", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["schedule_date"].widget = forms.DateInput(
            attrs={"type": "date", "class": "form-control"},
            format="%Y-%m-%d",
        )
        self.fields["status"].widget.attrs.update({"class": "form-control"})
        self.fields["description"].widget.attrs.update({"class": "form-control", "rows": 3})

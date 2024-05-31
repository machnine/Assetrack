"""equipment form module."""

from django import forms

from asset.models import Equipment


class EquipmentForm(forms.ModelForm):
    """Equipment form class"""
    class Meta:
        model = Equipment
        fields = "__all__"

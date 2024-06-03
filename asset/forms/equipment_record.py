"""equipment record form module."""

from django import forms

from asset.models import EquipmentRecord


class EquipmentRecordForm(forms.ModelForm):
    """EquipmentRecord form class"""
    class Meta:
        model = EquipmentRecord
        fields = ["date", "record_type", "description"]
"""CRUD view for equipment record"""

from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from asset.forms import EquipmentRecordForm
from asset.models import Equipment, EquipmentRecord


class EquipmentRecordListView(ListView):
    """List view for equipment record"""

    model = EquipmentRecord
    template_name = "asset/equipment_record_list.html"
    context_object_name = "records"

    def get_queryset(self):
        equipment_id = self.kwargs.get("equipment_id")
        return EquipmentRecord.objects.filter(equipment_id=equipment_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equipment_id = self.kwargs.get("equipment_id")
        context["equipment"] = Equipment.objects.get(id=equipment_id)
        return context


class EquipmentRecordCreateView(CreateView):
    """Create view for equipment record"""

    model = EquipmentRecord
    template_name = "asset/equipment_record_form.html"
    form_class = EquipmentRecordForm
    success_url = reverse_lazy("equipment_list")

    def form_valid(self, form):
        # get the equipment id from the url
        form.instance.equipment_id = self.kwargs.get("equipment_id")
        return super().form_valid(form)


class EquipmentRecordUpdateView(UpdateView):
    """Update view for equipment record"""

    model = EquipmentRecord
    template_name = "asset/equipment_record_form.html"
    form_class = EquipmentRecordForm
    context_object_name = "record"

    def get_success_url(self):
        return reverse_lazy("equipment_detail", kwargs={"pk": self.object.equipment.id})


class EquipmentRecordDeleteView(DeleteView):
    """Delete view for equipment record"""

    model = EquipmentRecord
    template_name = "asset/equipment_record_delete.html"
    context_object_name = "record"

    def get_success_url(self):
        return reverse_lazy("equipment_detail", kwargs={"pk": self.object.equipment.id})

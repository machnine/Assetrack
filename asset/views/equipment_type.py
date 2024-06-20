"""EquipmentType views"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from asset.forms import EquipmentTypeForm
from asset.models import EquipmentType


class EquipmentTypeListView(LoginRequiredMixin, ListView):
    """List view for the EquipmentType model"""

    model = EquipmentType
    template_name = "asset/equipmenttype_list.html"
    context_object_name = "eqipment_types"


class EquipmentTypeCreateView(LoginRequiredMixin, CreateView):
    """Create view for the EquipmentType model"""

    model = EquipmentType
    template_name = "asset/equipmenttype_form.html"
    form_class = EquipmentTypeForm
    success_url = reverse_lazy("equipmenttype_list")


class EquipmentTypeUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for the EquipmentType model"""

    model = EquipmentType
    template_name = "asset/equipmenttype_form.html"
    form_class = EquipmentTypeForm
    success_url = reverse_lazy("equipmenttype_list")


class EquipmentTypeDeleteView(LoginRequiredMixin, DeleteView):
    """Delete view for the EquipmentType model"""

    model = EquipmentType
    template_name = "partials/object_delete.html"
    success_url = reverse_lazy("equipmenttype_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse_lazy("equipmenttype_list")
        return context


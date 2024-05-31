""" CRUD operations for equipment """
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from asset.models import Equipment, EquipmentRecord

from asset.forms import EquipmentForm

class EquipmentListView(ListView):
    """List view for equipment"""

    model = Equipment
    template_name = "asset/equipment_list.html"
    context_object_name = "equipments"

class EquipmentCreateView(CreateView):
    """Create view for equipment"""

    model = Equipment
    template_name = "asset/equipment_form.html"
    form_class = EquipmentForm
    success_url = reverse_lazy("equipment_list")

class EquipmentDetailView(DetailView):
    """Detail view for equipment"""

    model = Equipment
    template_name = "asset/equipment_detail.html"
    context_object_name = "equipment"

class EquipmentUpdateView(UpdateView):
    """Update view for equipment"""

    model = Equipment
    template_name = "asset/equipment_form.html"
    form_class = EquipmentForm
    context_object_name = "equipment"

    def get_success_url(self):
        return reverse_lazy("equipment_detail", kwargs={"pk": self.object.id})
    
class EquipmentDeleteView(DeleteView):
    """Delete view for equipment"""

    model = Equipment
    template_name = "asset/equipment_delete.html"
    success_url = reverse_lazy("equipment_list")


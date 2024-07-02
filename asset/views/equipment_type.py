"""EquipmentType views"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from asset.forms import EquipmentTypeForm
from asset.models import EquipmentType


class EquipmentTypeListView(LoginRequiredMixin, ListView):
    """List view for the EquipmentType model"""

    model = EquipmentType
    template_name = "asset/equipmenttype_list.html"
    context_object_name = "eqipment_types"
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(description__icontains=query))
        return queryset.order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q")

        if query:
            context["query"] = f"Filter: {query}"

        return context

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


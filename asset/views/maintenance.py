"""maintenance record views"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from asset.forms import MaintenanceRecordForm, MaintenanceTaskForm
from asset.models import Equipment, MaintenanceRecord, MaintenanceTask


## Maintenance Record views
class MaintenanceRecordListView(ListView):
    model = MaintenanceRecord
    template_name = "asset/maintenance_record_list.html"
    context_object_name = "records"
    paginate_by = 16

    def get_queryset(self):
        queryset = MaintenanceRecord.objects.select_related("equipment").prefetch_related("maintenance__task")

        if equipment_type_id := self.request.GET.get("t", None):
            queryset = queryset.filter(equipment__equipment_type=equipment_type_id)

        return queryset


class MaintenanceRecordMixin:
    """Mixin for the maintenance record Create and Update views"""

    model = MaintenanceRecord
    form_class = MaintenanceRecordForm
    template_name = "asset/maintenance_record_form.html"
    success_url = reverse_lazy("maintenance_record_list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Filter equipment based on a query parameter or some logic
        equipment_type_id = self.request.GET.get("t", None)

        if equipment_type_id:
            filter = Q(equipment_type=equipment_type_id) & Q(status__name="Active")
        else:
            filter = Q(status__name="Active")

        form.fields["equipment"].queryset = Equipment.objects.filter(filter)

        return form


class MaintenanceRecordCreateView(MaintenanceRecordMixin, CreateView):
    pass


class MaintenanceRecordUpdateView(MaintenanceRecordMixin, UpdateView):
    pass


class MaintenanceRecordDeleteView(DeleteView):
    model = MaintenanceRecord
    template_name = "partials/object_delete.html"
    success_url = reverse_lazy("maintenance_record_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse_lazy("maintenance_record_list")
        return context


## Maintenance Task views
class MaintenanceTaskCreateView(LoginRequiredMixin, CreateView):
    """Create view for the maintenance task model"""

    model = MaintenanceTask
    template_name = "asset/maintenance_task_form.html"
    form_class = MaintenanceTaskForm
    success_url = reverse_lazy("maintenance_task_list")


class MaintenanceTaskListView(LoginRequiredMixin, ListView):
    """List view for the maintenance task model"""

    model = MaintenanceTask
    template_name = "asset/maintenance_task_list.html"


class MaintenanceTaskUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for the maintenance task model"""

    model = MaintenanceTask
    template_name = "asset/maintenance_task_form.html"
    form_class = MaintenanceTaskForm
    success_url = reverse_lazy("maintenance_task_list")


class MaintenanceTaskDeleteView(LoginRequiredMixin, DeleteView):
    """Delete view for the maintenance task model"""

    model = MaintenanceTask
    template_name = "partials/object_delete.html"
    success_url = reverse_lazy("maintenance_task_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse_lazy("maintenance_task_list")
        return context

"""maintenance record views"""

from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from asset.models import MaintenanceRecord, MaintenanceRecordAssignment, MaintenanceTask, Equipment

from asset.forms import MaintenanceTaskForm, MaintenanceRecordForm


## Maintenance Record views


class MaintenanceRecordCreateView(CreateView):
    model = MaintenanceRecord
    form_class = MaintenanceRecordForm
    template_name = "asset/maintenance_record_form.html"
    success_url = reverse_lazy("maintenance_record_list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Filter equipment based on a query parameter or some logic
        equipment_type = self.request.GET.get("equipment_type", None)

        if equipment_type:
            form.fields["equipment"].queryset = Equipment.objects.filter(
                equipment_type__name=equipment_type, status__name="Active"
            )
        else:
            form.fields["equipment"].queryset = Equipment.objects.filter(status__name="Active")

        return form


class MaintenanceRecordListView(ListView):
    model = MaintenanceRecord
    template_name = "asset/maintenance_record_list.html"
    context_object_name = "records"
    paginate_by = 10

    def get_queryset(self):
        return MaintenanceRecord.objects.all().order_by("-date")


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

"""maintenance record views"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from asset.forms import MaintenanceRecordForm, MaintenanceTaskForm
from asset.models import Equipment, EquipmentType, MaintenanceRecord, MaintenanceRecordAssignment, MaintenanceTask, SiteConfiguration


## Maintenance Record views
class MaintenanceRecordListView(LoginRequiredMixin, ListView):
    model = MaintenanceRecord
    template_name = "asset/maintenance_record_list.html"
    context_object_name = "records"
    paginate_by = int(SiteConfiguration.get_value("PAGINATION_MAINTENANCE_RECORD_LIST") or 16)

    def get_queryset(self):
        queryset = MaintenanceRecord.objects.select_related("equipment").prefetch_related("maintenance__task")
        equipment_type_slug = self.kwargs.get("slug")

        if equipment_type_slug:
            queryset = queryset.filter(equipment__equipment_type__slug=equipment_type_slug)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get("slug")
        context["equipment_type"] = EquipmentType.objects.get(slug=slug)
        return context


class MaintenanceRecordMixin(LoginRequiredMixin):
    """Mixin for the maintenance record Create, Update and Delete views"""

    model = MaintenanceRecord
    form_class = MaintenanceRecordForm
    template_name = "asset/maintenance_record_form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        equipment_type_slug = self.kwargs.get("slug")

        if form.instance.pk and form.instance.equipment:
            equipment_type_slug = form.instance.equipment.equipment_type.slug

        if equipment_type_slug:
            form.fields["equipment"].queryset = Equipment.objects.filter(
                equipment_type__slug=equipment_type_slug, status__name="Active"
            )
            form.fields["tasks"].queryset = MaintenanceTask.objects.filter(equipment_type__slug=equipment_type_slug)

        # Pre-select tasks already associated with the record
        if form.instance.pk:
            form.fields["tasks"].initial = self.object.maintenance.values_list("task", flat=True)

        return form

    def _save_tasks(self, tasks):
        for task in tasks:
            MaintenanceRecordAssignment.objects.create(maintenance=self.object, task=task)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get("slug")
        context["equipment_type_slug"] = slug
        context["equipment_type"] = EquipmentType.objects.get(slug=slug)
        return context

    def get_success_url(self):
        return reverse("maintenance_record_list", kwargs={"slug": self.kwargs.get("slug")})


class MaintenanceRecordCreateView(MaintenanceRecordMixin, CreateView):
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        self.object = form.save()

        self._save_tasks(form.cleaned_data.get("tasks"))
        return redirect(self.get_success_url())


class MaintenanceRecordUpdateView(MaintenanceRecordMixin, UpdateView):
    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        self.object = form.save()

        # Clear existing tasks and reassign selected ones
        MaintenanceRecordAssignment.objects.filter(maintenance=self.object).delete()

        self._save_tasks(form.cleaned_data.get("tasks"))
        return redirect(self.get_success_url())


class MaintenanceRecordDeleteView(LoginRequiredMixin, DeleteView):
    model = MaintenanceRecord
    template_name = "partials/object_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = self.get_success_url()
        return context

    def get_success_url(self) -> str:
        return reverse("maintenance_record_list", kwargs={"slug": self.kwargs.get("slug")})


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
    paginate_by = int(SiteConfiguration.get_value("PAGINATION_MAINTENANCE_TASK_LIST") or 16)

    def get_queryset(self):
        queryset = super().get_queryset()
        if equipment_type := self.request.GET.get("t"):
            queryset = queryset.filter(equipment_type__pk=equipment_type)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if equipment_type := self.request.GET.get("t"):
            context["query"] = EquipmentType.objects.get(pk=equipment_type)
        return context


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


# Maintenance How-Tos views
class LxMaintenanceHowToView(TemplateView):
    """
    How-to guide for LX maintenance
    """

    def get_template_names(self):
        task = self.kwargs.get("task")
        if task in ["daily", "fortnightly", "long-term"]:
            return f"asset/maintenance_howto_lx_{task}.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = self.kwargs.get("task")
        context["equipment"] = "Luminex"
        return context

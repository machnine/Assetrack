"""status crud views"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from asset.forms import StatusForm
from asset.models import Status


class StatusListView(LoginRequiredMixin, ListView):
    """List view for the status model"""

    model = Status
    template_name = "asset/status_list.html"
    context_object_name = "statuses"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(equipment_count=Count("equipment")).order_by("-equipment_count")
        return queryset


class StatusCreateView(LoginRequiredMixin, CreateView):
    """Create view for the status model"""

    model = Status
    template_name = "asset/status_form.html"
    form_class = StatusForm
    success_url = reverse_lazy("status_list")


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for the status model"""

    model = Status
    template_name = "asset/status_form.html"
    form_class = StatusForm
    success_url = reverse_lazy("status_list")


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    """Delete view for the status model"""

    model = Status
    template_name = "partials/object_delete.html"
    success_url = reverse_lazy("status_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse_lazy("status_list")
        return context

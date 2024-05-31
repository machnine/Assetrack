"""status crud views"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from asset.models import Status


class StatusListView(LoginRequiredMixin, ListView):
    """List view for the status model"""

    model = Status
    template_name = "asset/status_list.html"
    context_object_name = "statuses"


class StatusCreateView(LoginRequiredMixin, CreateView):
    """Create view for the status model"""

    model = Status
    template_name = "asset/status_form.html"
    fields = ["name", "description"]
    success_url = reverse_lazy("status_list")


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for the status model"""

    model = Status
    template_name = "asset/status_form.html"
    fields = ["name", "description"]
    success_url = reverse_lazy("status_list")


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    """Delete view for the status model"""

    model = Status
    template_name = "asset/status_delete.html"
    success_url = reverse_lazy("status_list")

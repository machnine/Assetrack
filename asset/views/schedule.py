"""CRUD views for Asset Schedule"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from asset.forms import ScheduleForm
from asset.models import Schedule


class ScheduleCreateView(LoginRequiredMixin, CreateView):
    """Create view for Schedule"""

    model = Schedule
    form_class = ScheduleForm
    template_name = "asset/schedule_form.html"
    success_url = reverse_lazy("schedule_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ScheduleListView(LoginRequiredMixin, ListView):
    """List view for Schedule"""

    model = Schedule
    template_name = "asset/schedule_list.html"
    context_object_name = "schedules"

    def get_context_data(self, **kwargs):
        """only show schedules >= today"""
        context = super().get_context_data(**kwargs)
        context["schedules"] = Schedule.objects.filter(schedule_date__gte=timezone.now())
        return context


class ScheduleUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for Schedule"""

    model = Schedule
    form_class = ScheduleForm
    template_name = "asset/schedule_form.html"
    success_url = reverse_lazy("schedule_list")


class ScheduleDeleteView(LoginRequiredMixin, DeleteView):
    """Delete view for Schedule"""

    model = Schedule
    template_name = "partials/object_delete.html"
    success_url = reverse_lazy("schedule_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_name"] = str(self.get_object())
        context["cancel_url"] = reverse_lazy("schedule_list")
        return context

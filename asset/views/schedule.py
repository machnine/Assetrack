"""CRUD views for Asset Schedule"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import HttpResponse, HttpResponseRedirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from asset.forms import ScheduleForm
from asset.models import Schedule, SiteConfiguration


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
    paginate_by = int(SiteConfiguration.get_value("PAGINATION_SCHEDULE_LIST") or 16)

    def get_queryset(self):
        """
        Return the schedules for the last 4 weeks and upcoming.
        """
        query_set = super().get_queryset()
        show_all = self.request.GET.get("all")
        q = self.request.GET.get("q")
        two_weeks_ago = timezone.now() - timezone.timedelta(weeks=4)

        # Build Q objects for filters
        filters = Q(schedule_date__gte=two_weeks_ago)

        if q:
            filters &= Q(description__icontains=q)

        if show_all != "true":
            filters &= Q(status="A")

        # Apply the filters to the queryset
        query_set = query_set.filter(filters).order_by("schedule_date")

        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["today"] = timezone.now().date()
        return context


class ScheduleUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for Schedule"""

    model = Schedule
    form_class = ScheduleForm
    template_name = "asset/schedule_form.html"
    success_url = reverse_lazy("schedule_list")

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


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


class ScheduleActionView(LoginRequiredMixin, View):
    """Action view for Schedule to update status or recurrence"""

    def post(self, request, *args, **kwargs):
        schedule = get_object_or_404(Schedule, pk=kwargs.get("pk"))

        # Update updated_by
        schedule.updated_by = request.user
        # Mark as completed or move to next date
        schedule.update_scheduel_status()

        if request.htmx:
            if schedule.frequency == "O":  # One-off schedule
                return HttpResponse("")
            else:
                return render(
                    request, "partials/asset/schedule_item.html", {"schedule": schedule, "highlighted": "highlighted"}
                )
        return HttpResponseRedirect(reverse_lazy("schedule_list"))

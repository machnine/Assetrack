"""views for software records"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from asset.forms import SoftwareRecordForm
from asset.models import SoftwareRecord


class SoftwareRecordCreateView(LoginRequiredMixin, CreateView):
    """Create view for software record"""

    model = SoftwareRecord
    template_name = "asset/softwarerecord_form.html"
    form_class = SoftwareRecordForm

    def form_valid(self, form):
        # get the software id from the url
        form.instance.software_id = self.kwargs.get("software_id")
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("software_detail", kwargs={"pk": self.object.software.id})


class SoftwareRecordUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for software record"""

    model = SoftwareRecord
    template_name = "asset/softwarerecord_form.html"
    form_class = SoftwareRecordForm
    context_object_name = "record"

    def form_valid(self, form):
        form.instance.last_updated_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("software_detail", kwargs={"pk": self.object.software.id})


class SoftwareRecordDeleteView(LoginRequiredMixin, DeleteView):
    """Delete view for software record"""

    model = SoftwareRecord
    template_name = "partials/object_delete.html"
    context_object_name = "record"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse_lazy("software_detail", kwargs={"pk": self.object.software.id})
        return context

    def get_success_url(self):
        return reverse_lazy("software_detail", kwargs={"pk": self.object.software.id})

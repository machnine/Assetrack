"""views associated with the Location model"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from asset.forms import LocationForm
from asset.models import Location


class LocationListView(LoginRequiredMixin, ListView):
    """List view for the location model"""

    model = Location
    template_name = "asset/location_list.html"
    context_object_name = "locations"


class LocationCreateView(LoginRequiredMixin, CreateView):
    """Create view for the location model"""

    model = Location
    template_name = "asset/location_form.html"
    form_class = LocationForm
    success_url = reverse_lazy("location_list")


class LocationUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for the location model"""

    model = Location
    template_name = "asset/location_form.html"
    form_class = LocationForm
    success_url = reverse_lazy("location_list")


class LocationDeleteView(LoginRequiredMixin, DeleteView):
    """Delete view for the location model"""

    model = Location
    template_name = "partials/object_delete.html"
    success_url = reverse_lazy("location_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse_lazy("location_list")
        return context

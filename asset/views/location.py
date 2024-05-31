"""views associated with the Location model"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

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
    fields = ["name", "description"]
    success_url = reverse_lazy("location_list")


class LocationUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for the location model"""

    model = Location
    template_name = "asset/location_form.html"
    fields = ["name", "description"]
    success_url = reverse_lazy("location_list")


class LocationDeleteView(LoginRequiredMixin, DeleteView):
    """Delete view for the location model"""

    model = Location
    template_name = "asset/location_delete.html"
    success_url = reverse_lazy("location_list")

"""CRUD operations for equipment"""

import re

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from asset.forms import EquipmentAttachmentUpdateForm, EquipmentAttachmentUploadForm, EquipmentForm
from asset.models import Calibration, Category, Company, Equipment, EquipmentAttachment, EquipmentType, Location, Status
from attachment.views import AttachmentDeleteView, AttachmentUpdateView, AttachmentUploadView


class EquipmentListView(LoginRequiredMixin, ListView):
    """List view for equipment"""

    model = Equipment
    template_name = "asset/equipment_list.html"
    context_object_name = "equipments"
    paginate_by = 16

    def get_queryset(self):
        queryset = super().get_queryset()
        filters = {
            "q": self.request.GET.get("q"),
            "manufacturer_id": self.request.GET.get("m"),
            "location_id": self.request.GET.get("l"),
            "status_id": self.request.GET.get("s"),
            "category_id": self.request.GET.get("c"),
            "equipment_type_id": self.request.GET.get("t"),
            "service_provider_id": self.request.GET.get("sp"),
            "calibration_id": self.request.GET.get("cal"),
            "replacement": self.request.GET.get("rp"),
            "model_number": self.request.GET.get("n"),
            "show_all": self.request.GET.get("all"),
        }

        # normalise the query string
        if filters["q"]:
            filters["q"] = re.sub(r"[^A-Za-z0-9 ]+", "", filters["q"]).strip()

        queries = {
            "q": Q(name__icontains=filters["q"]) | Q(notes__icontains=filters["q"]),
            "manufacturer_id": Q(manufacturer_id=filters["manufacturer_id"]),
            "location_id": Q(location_id=filters["location_id"]),
            "status_id": Q(status_id=filters["status_id"]),
            "category_id": Q(category_id=filters["category_id"]),
            "equipment_type_id": Q(equipment_type_id=filters["equipment_type_id"]),
            "service_provider_id": Q(service_provider_id=filters["service_provider_id"]),
            "calibration_id": Q(calibration_id=filters["calibration_id"]),
            "model_number": Q(model_number__icontains=filters["model_number"]),
        }

        # Remove queries with None values
        filtered_queries = {key: query for key, query in queries.items() if filters[key]}

        for query in filtered_queries.values():
            queryset = queryset.filter(query)

        # Apply the special 'replacement' filter
        if filters["replacement"] == "true":
            one_year_from_now = timezone.now() + timezone.timedelta(days=365)
            queryset = queryset.filter(replacement_date__lte=one_year_from_now).exclude(status__name="Decommissioned")
        else:
            # Apply default exclusion of 'Decommissioned' status unless 'show_all' is true
            if filters["show_all"] != "true":
                queryset = queryset.exclude(status__name="Decommissioned")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.get_filter_description()
        return context

    def get_filter_description(self):
        descriptions = {
            "q": ("Search Filter", self.request.GET.get("q")),
            "m": ("Manufacturer", self.get_object_description(Company, self.request.GET.get("m"))),
            "l": ("Location", self.get_object_description(Location, self.request.GET.get("l"))),
            "s": ("Status", self.get_object_description(Status, self.request.GET.get("s"))),
            "c": ("Category", self.get_object_description(Category, self.request.GET.get("c"))),
            "t": ("Equipment Type", self.get_object_description(EquipmentType, self.request.GET.get("t"))),
            "sp": ("Service Provider", self.get_object_description(Company, self.request.GET.get("sp"))),
            "cal": ("Calibration", self.get_object_description(Calibration, self.request.GET.get("cal"))),
            "rp": ("Replacement due in 365 days", self.request.GET.get("rp")),
            "n": ("Model Number", self.request.GET.get("n")),
        }

        descriptions = [f"{label}: {value}" for key, (label, value) in descriptions.items() if value]
        return ", ".join(descriptions)

    def get_object_description(self, model, object_id):
        if object_id:
            try:
                return model.objects.get(id=object_id)
            except model.DoesNotExist:
                return None
        return None


class EquipmentCreateView(LoginRequiredMixin, CreateView):
    """Create view for equipment"""

    model = Equipment
    template_name = "asset/equipment_form.html"
    form_class = EquipmentForm
    success_url = reverse_lazy("equipment_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class EquipmentDetailView(LoginRequiredMixin, DetailView):
    """Detail view for equipment"""

    model = Equipment
    template_name = "asset/equipment_detail.html"
    context_object_name = "equipment"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["attachments"] = EquipmentAttachment.objects.filter(object_id=self.object.id)
        return context


class EquipmentUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for equipment"""

    model = Equipment
    template_name = "asset/equipment_form.html"
    form_class = EquipmentForm
    context_object_name = "equipment"

    def form_valid(self, form):
        form.instance.last_updated_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """return the URL to redirect to, after processing a valid form."""

        if next_url := self.request.POST.get("next") or self.request.GET.get("next"):
            return next_url
        else:
            return reverse_lazy("equipment_detail", kwargs={"pk": self.object.id})


class EquipmentDeleteView(LoginRequiredMixin, DeleteView):
    """Delete view for equipment"""

    model = Equipment
    template_name = "partials/object_delete.html"
    success_url = reverse_lazy("equipment_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse_lazy("equipment_list")
        return context


### EquipmentAttachment CRUD operations


class EquipmentAttachmentUploadView(LoginRequiredMixin, AttachmentUploadView):
    """Upload view for equipment attachments"""

    owner_model = Equipment
    form_class = EquipmentAttachmentUploadForm
    template_name = "attachment/attachment_upload_form.html"
    success_url_name = "equipment_detail"


class EquipmentAttachmentUpdateView(LoginRequiredMixin, AttachmentUpdateView):
    """Update view for equipment attachments"""

    owner_model = Equipment
    model = EquipmentAttachment
    form_class = EquipmentAttachmentUpdateForm
    template_name = "attachment/attachment_update_form.html"
    success_url_name = "equipment_detail"


class EquipmentAttachmentDeleteView(LoginRequiredMixin, AttachmentDeleteView):
    """Delete view for equipment attachments"""

    owner_model = Equipment
    model = EquipmentAttachment
    success_url_name = "equipment_detail"
    template_name = "attachment/attachment_delete_form.html"

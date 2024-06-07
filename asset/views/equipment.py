"""CRUD operations for equipment"""

from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from asset.forms import EquipmentAttachmentUpdateForm, EquipmentAttachmentUploadForm, EquipmentForm
from asset.models import Category, Company, Equipment, EquipmentAttachment, Location, Status
from attachment.views import AttachmentDeleteView, AttachmentUpdateView, AttachmentUploadView


class EquipmentListView(ListView):
    """List view for equipment"""

    model = Equipment
    template_name = "asset/equipment_list.html"
    context_object_name = "equipments"

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        manufacturer = self.request.GET.get("m")
        service_provider = self.request.GET.get("sp")
        location = self.request.GET.get("l")
        status = self.request.GET.get("s")
        category = self.request.GET.get("c")

        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(notes__icontains=query))
        if manufacturer:
            queryset = queryset.filter(manufacturer_id=manufacturer)
        if location:
            queryset = queryset.filter(location_id=location)
        if status:
            queryset = queryset.filter(status_id=status)
        if category:
            queryset = queryset.filter(category_id=category)
        if service_provider:
            queryset = queryset.filter(service_provider_id=service_provider)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q")
        manufacturer = self.request.GET.get("m")
        location = self.request.GET.get("l")
        status = self.request.GET.get("s")
        category = self.request.GET.get("c")
        service_provider = self.request.GET.get("sp")

        if query:
            query = f"Filter: {query}"
        if manufacturer:
            query = f"Manufacturer: {Company.objects.get(id=manufacturer)}"
        if location:
            query = f"Location: {Location.objects.get(id=location)}"
        if status:
            query = f"Status: {Status.objects.get(id=status)}"
        if category:
            query = f"Category: {Category.objects.get(id=category)}"
        if service_provider:
            query = f"Service Provider: {Company.objects.get(id=service_provider)}"

        context["query"] = query

        return context


class EquipmentCreateView(CreateView):
    """Create view for equipment"""

    model = Equipment
    template_name = "asset/equipment_form.html"
    form_class = EquipmentForm
    success_url = reverse_lazy("equipment_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class EquipmentDetailView(DetailView):
    """Detail view for equipment"""

    model = Equipment
    template_name = "asset/equipment_detail.html"
    context_object_name = "equipment"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["attachments"] = EquipmentAttachment.objects.filter(object_id=self.object.id)
        return context


class EquipmentUpdateView(UpdateView):
    """Update view for equipment"""

    model = Equipment
    template_name = "asset/equipment_form.html"
    form_class = EquipmentForm
    context_object_name = "equipment"

    def form_valid(self, form):
        print(form.instance.created_by)
        form.instance.last_updated_by = self.request.user
        print(form.instance.created_by)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("equipment_detail", kwargs={"pk": self.object.id})


class EquipmentDeleteView(DeleteView):
    """Delete view for equipment"""

    model = Equipment
    template_name = "partials/object_delete.html"
    success_url = reverse_lazy("equipment_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse_lazy("equipment_list")
        return context


### EquipmentAttachment CRUD operations


class EquipmentAttachmentUploadView(AttachmentUploadView):
    """Upload view for equipment attachments"""

    owner_model = Equipment
    form_class = EquipmentAttachmentUploadForm
    template_name = "attachment/attachment_upload_form.html"
    success_url_name = "equipment_detail"


class EquipmentAttachmentUpdateView(AttachmentUpdateView):
    """Update view for equipment attachments"""

    owner_model = Equipment
    model = EquipmentAttachment
    form_class = EquipmentAttachmentUpdateForm
    template_name = "attachment/attachment_update_form.html"
    success_url_name = "equipment_detail"


class EquipmentAttachmentDeleteView(AttachmentDeleteView):
    """Delete view for equipment attachments"""

    owner_model = Equipment
    model = EquipmentAttachment
    success_url_name = "equipment_detail"
    template_name = "attachment/attachment_delete_form.html"

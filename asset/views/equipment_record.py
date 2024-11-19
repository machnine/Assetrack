"""CRUD view for equipment record"""

import re
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView, ListView

from asset.forms import EquipmentRecordAttachmentUpdateForm, EquipmentRecordAttachmentUploadForm, EquipmentRecordForm
from asset.models import EquipmentRecord, SiteConfiguration
from asset.models.record import EquipmentRecordAttachment
from attachment.views import AttachmentDeleteView, AttachmentUpdateView, AttachmentUploadView

class EquipmentRecordListView(LoginRequiredMixin, ListView):
    """List view for equipment record"""

    model = EquipmentRecord
    template_name = "asset/equipmentrecord_list.html"
    context_object_name = "records"
    paginate_by = int(SiteConfiguration.get_value("PAGINATION_EQUIPMENT_RECORD") or 16)    

    def get_queryset(self):
        queryset = super().get_queryset()
        filters = {"q": self.request.GET.get("q"), "record_type": self.request.GET.get("type")}

        # normalise the query string
        if filters["q"]:
            filters["q"] = re.sub(r"[^A-Za-z0-9 ]+", "", filters["q"]).strip()

        queries = {
            "q": Q(equipment__name__icontains=filters["q"])| Q(description__icontains=filters["q"]),            
            "record_type": Q(record_type=filters["record_type"])}
        
        # Remove queries with None values
        filtered_queries = {key: query for key, query in queries.items() if filters[key]}

        for query in filtered_queries.values():
            queryset = queryset.filter(query)
        
        return queryset


class EquipmentRecordCreateView(LoginRequiredMixin, CreateView):
    """Create view for equipment record"""

    model = EquipmentRecord
    template_name = "asset/equipmentrecord_form.html"
    form_class = EquipmentRecordForm

    def form_valid(self, form):
        # get the equipment id from the url
        form.instance.equipment_id = self.kwargs.get("equipment_id")
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("equipment_detail", kwargs={"pk": self.object.equipment.id})


class EquipmentRecordUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for equipment record"""

    model = EquipmentRecord
    template_name = "asset/equipmentrecord_form.html"
    form_class = EquipmentRecordForm
    context_object_name = "record"

    def form_valid(self, form):
        form.instance.last_updated_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("equipment_detail", kwargs={"pk": self.object.equipment.id})


class EquipmentRecordDeleteView(LoginRequiredMixin, DeleteView):
    """Delete view for equipment record"""

    model = EquipmentRecord
    template_name = "partials/object_delete.html"
    context_object_name = "record"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse_lazy("equipment_detail", kwargs={"pk": self.object.equipment.id})
        return context

    def get_success_url(self):
        return reverse_lazy("equipment_detail", kwargs={"pk": self.object.equipment.id})


class EquipmentRecordDetailView(LoginRequiredMixin, DetailView):
    """Detail view for equipment record"""

    model = EquipmentRecord
    template_name = "asset/equipmentrecord_detail.html"
    context_object_name = "record"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["attachments"] = EquipmentRecordAttachment.objects.filter(object_id=self.object.id)
        return context


### EquipmentRecordAttachment CRUD operations


class EquipmentRecordAttachmentUploadView(LoginRequiredMixin, AttachmentUploadView):
    """Upload view for equipment record attachments"""

    owner_model = EquipmentRecord
    form_class = EquipmentRecordAttachmentUploadForm
    template_name = "attachment/upload_form.html"
    success_url_name = "equipmentrecord_detail"


class EquipmentRecordAttachmentUpdateView(LoginRequiredMixin, AttachmentUpdateView):
    """Update view for equipment record attachments"""

    owner_model = EquipmentRecord
    model = EquipmentRecordAttachment
    form_class = EquipmentRecordAttachmentUpdateForm
    template_name = "attachment/update_form.html"
    success_url_name = "equipmentrecord_detail"


class EquipmentRecordAttachmentDeleteView(LoginRequiredMixin, AttachmentDeleteView):
    """Delete view for equipment record attachments"""

    owner_model = EquipmentRecord
    model = EquipmentRecordAttachment
    success_url_name = "equipmentrecord_detail"
    template_name = "attachment/delete_form.html"

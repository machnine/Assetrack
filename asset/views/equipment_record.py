"""CRUD view for equipment record"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from asset.forms import EquipmentRecordAttachmentUpdateForm, EquipmentRecordAttachmentUploadForm, EquipmentRecordForm
from asset.models import Equipment, EquipmentRecord
from asset.models.record import EquipmentRecordAttachment
from attachment.views import AttachmentDeleteView, AttachmentUpdateView, AttachmentUploadView


class EquipmentRecordListView(LoginRequiredMixin, ListView):
    """List view for equipment record"""

    model = EquipmentRecord
    template_name = "asset/equipmentrecord_list.html"
    context_object_name = "records"

    def get_queryset(self):
        equipment_id = self.kwargs.get("equipment_id")
        return EquipmentRecord.objects.filter(equipment_id=equipment_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equipment_id = self.kwargs.get("equipment_id")
        context["equipment"] = Equipment.objects.get(id=equipment_id)
        return context


class EquipmentRecordCreateView(LoginRequiredMixin, CreateView):
    """Create view for equipment record"""

    model = EquipmentRecord
    template_name = "asset/equipmentrecord_form.html"
    form_class = EquipmentRecordForm
    success_url = reverse_lazy("equipment_list")

    def form_valid(self, form):
        # get the equipment id from the url
        form.instance.equipment_id = self.kwargs.get("equipment_id")
        return super().form_valid(form)


class EquipmentRecordUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for equipment record"""

    model = EquipmentRecord
    template_name = "asset/equipmentrecord_form.html"
    form_class = EquipmentRecordForm
    context_object_name = "record"

    def get_success_url(self):
        return reverse_lazy("equipment_detail", kwargs={"pk": self.object.equipment.id})


class EquipmentRecordDeleteView(LoginRequiredMixin, DeleteView):
    """Delete view for equipment record"""

    model = EquipmentRecord
    template_name = "asset/equipmentrecord_delete.html"
    context_object_name = "record"

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


class EquipmentRecordAttachmentUploadView(AttachmentUploadView):
    """Upload view for equipment record attachments"""

    owner_model = EquipmentRecord
    form_class = EquipmentRecordAttachmentUploadForm
    template_name = "attachment/attachment_upload_form.html"
    success_url_name = "equipmentrecord_detail"


class EquipmentRecordAttachmentUpdateView(AttachmentUpdateView):
    """Update view for equipment record attachments"""

    owner_model = EquipmentRecord
    model = EquipmentRecordAttachment
    form_class = EquipmentRecordAttachmentUpdateForm
    template_name = "attachment/attachment_update_form.html"
    success_url_name = "equipmentrecord_detail"


class EquipmentRecordAttachmentDeleteView(AttachmentDeleteView):
    """Delete view for equipment record attachments"""

    owner_model = EquipmentRecord
    model = EquipmentRecordAttachment
    success_url_name = "equipmentrecord_detail"
    template_name = "attachment/attachment_delete_form.html"

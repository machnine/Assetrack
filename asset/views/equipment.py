"""CRUD operations for equipment"""

from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from asset.forms import EquipmentAttachmentUpdateForm, EquipmentAttachmentUploadForm, EquipmentForm
from asset.models import Equipment, EquipmentAttachment
from attachment.views import AttachmentDeleteView, AttachmentUpdateView, AttachmentUploadView


class EquipmentListView(ListView):
    """List view for equipment"""

    model = Equipment
    template_name = "asset/equipment_list.html"
    context_object_name = "equipments"


class EquipmentCreateView(CreateView):
    """Create view for equipment"""

    model = Equipment
    template_name = "asset/equipment_form.html"
    form_class = EquipmentForm
    success_url = reverse_lazy("equipment_list")


class EquipmentDetailView(DetailView):
    """Detail view for equipment"""

    model = Equipment
    template_name = "asset/equipment_detail.html"
    context_object_name = "equipment"


class EquipmentUpdateView(UpdateView):
    """Update view for equipment"""

    model = Equipment
    template_name = "asset/equipment_form.html"
    form_class = EquipmentForm
    context_object_name = "equipment"

    def get_success_url(self):
        return reverse_lazy("equipment_detail", kwargs={"pk": self.object.id})


class EquipmentDeleteView(DeleteView):
    """Delete view for equipment"""

    model = Equipment
    template_name = "asset/equipment_delete.html"
    success_url = reverse_lazy("equipment_list")


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

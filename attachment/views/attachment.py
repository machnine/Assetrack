"""Views for the attachment app."""

from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import View


class AttachmentActionUrlNameMixin:
    """Mixin to add action url names to a view."""

    owner_model = None

    def get_form_action_url_name(self, action: str):
        """Return the url name for the form action."""
        owner_model_name = self.owner_model._meta.model_name
        return f"{owner_model_name}_attachment_{action}"


class AttachmentUploadView(AttachmentActionUrlNameMixin, View):
    """Generic view to upload attachments to a given object."""

    form_class = None
    template_name = None
    success_url_name = None

    def get_owner_object(self, pk):
        """Get the owner object."""
        return get_object_or_404(self.owner_model, pk=pk)

    def get(self, request, pk):
        form = self.form_class()
        url_name = self.get_form_action_url_name("upload")
        upload_url = reverse_lazy(url_name, kwargs={"pk": pk})
        return render(request, self.template_name, {"form": form, "upload_url": upload_url})

    def post(self, request, pk):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            # log uploaded_by user
            form.instance.uploaded_by = request.user
            
            attachment = form.save(commit=False)
            attachment.content_object = get_object_or_404(self.owner_model, pk=pk)
            attachment.save()
            messages.success(request, f"Attachment {attachment.filename} uploaded successfully!")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Upload {field.capitalize()}: {error}")
        return redirect(reverse_lazy(self.success_url_name, kwargs={"pk": pk}))


class AttachmentUpdateView(AttachmentActionUrlNameMixin, View):
    """Generic view to edit attachments associated with a given object."""

    model = None
    form_class = None
    template_name = None
    success_url_name = None

    def get(self, request, pk):
        attachment = get_object_or_404(self.model, pk=pk)
        form = self.form_class(instance=attachment)
        return render(
            request,
            self.template_name,
            {"form": form, "attachment": attachment, "action_url_name": self.get_form_action_url_name("update")},
        )

    def post(self, request, pk):
        attachment = get_object_or_404(self.model, pk=pk)
        form = self.form_class(request.POST, request.FILES, instance=attachment)
        if form.is_valid():
            attachment = form.save()
            messages.success(request, f"Attachment {attachment.filename} updated successfully!")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Upload {field.capitalize()}: {error}")
        return redirect(reverse_lazy(self.success_url_name, kwargs={"pk": attachment.object_id}))


class AttachmentDeleteView(AttachmentActionUrlNameMixin, View):
    """HTMX powered view to delete attachments associated with a given object."""

    model = None
    template_name = None
    success_url_name = None

    def get(self, request, *args, **kwargs):
        """HTMX GET request for returning an Attachment delete form."""
        attachment = get_object_or_404(self.model, pk=kwargs["pk"])
        return render(
            request,
            self.template_name,
            {"attachment": attachment, "action_url_name": self.get_form_action_url_name("delete")},
        )

    def post(self, request, *args, **kwargs):
        """HTMX POST request for deleting an Attachment."""
        attachment = get_object_or_404(self.model, pk=kwargs["pk"])
        # delete from the database
        owner_object_id = attachment.object_id  # get the id of the related object before the attachment is deleted
        attachment.delete()
        # Delete the file from the file system
        file_path = Path(settings.MEDIA_ROOT) / attachment.file.name
        if file_path.is_file():
            file_path.unlink()
        messages.success(request, f"Attachment {attachment.filename} deleted successfully!")

        return redirect(self.get_owner_redirect_url(owner_object_id))

    def get_owner_redirect_url(self, owner_object_id):
        """Return the url to redirect to after the attachment is deleted."""
        return reverse_lazy(self.success_url_name, kwargs={"pk": owner_object_id})

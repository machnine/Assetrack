from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, View

from attachment.forms import DocumentForm
from attachment.models import Document


class DocumentListView(ListView):
    """View to list documents"""

    template_name = "attachment/document_list.html"
    model = Document
    context_object_name = "documents"


class DocumentUploadView(View):
    """View to upload documents"""

    template_name = "attachment/upload_form.html"
    success_url = reverse_lazy("document_list")

    def get(self, request):
        form = DocumentForm()
        action_url = reverse_lazy("document_upload")
        return render(request, self.template_name, {"form": form, "upload_url": action_url})

    def post(self, request):
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            if request.user.is_authenticated:
                document.uploaded_by = request.user
            document.save()
            messages.success(request, f"Document {document.filename} uploaded successfully!")
            return redirect(self.success_url)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Upload {field.capitalize()}: {error}")
        return render(request, self.template_name, {"form": form})


class DocumentUpdateView(View):
    """View to update documents"""

    template_name = "attachment/update_form.html"
    success_url = reverse_lazy("document_list")

    def get(self, request, pk):
        document = get_object_or_404(Document, pk=pk)
        form = DocumentForm(instance=document)
        return render(
            request, self.template_name, {"form": form, "attachment": document, "action_url_name": "document_update"}
        )

    def post(self, request, pk):
        document = get_object_or_404(Document, pk=pk)
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            document = form.save()
            messages.success(request, f"Document {document.filename} updated successfully!")
            return redirect(self.success_url)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Update {field.capitalize()}: {error}")
        return render(request, self.template_name, {"form": form, "document": document})


class DocumentDeleteView(View):
    """View to delete documents"""

    template_name = "attachment/delete_form.html"
    success_url = reverse_lazy("document_list")

    def get(self, request, pk):
        document = get_object_or_404(Document, pk=pk)
        return render(request, self.template_name, {"attachment": document, "action_url_name": "document_delete"})

    def post(self, request, pk):
        document = get_object_or_404(Document, pk=pk)
        document.delete()
        # Delete the file from the file system
        file_path = Path(settings.MEDIA_ROOT) / document.file.name
        if file_path.is_file():
            file_path.unlink()
        messages.success(request, f"Document {document.filename} deleted successfully!")
        return redirect(self.success_url)

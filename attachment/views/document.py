"""Views for the document object"""

import re
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, View

from attachment.forms import DocumentForm
from attachment.models import Document


class DocumentListView(LoginRequiredMixin, ListView):
    """View to list documents"""

    model = Document
    template_name = "attachment/document_list.html"
    context_object_name = "documents"

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get("q")
        if q:
            q = re.sub(r"[^A-Za-z0-9 ]+", "", q).strip()
            query = Q(name__icontains=q) | Q(description__icontains=q)
            queryset = queryset.filter(query)
        return queryset


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
            document.save()
            messages.success(request, f"Document {document.filename} uploaded successfully!")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Upload {field.capitalize()}: {error}")
        return redirect(self.success_url)


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
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Update {field.capitalize()}: {error}")
        return redirect(self.success_url)


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

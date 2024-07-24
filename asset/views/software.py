"""software related views"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from asset.forms import SoftwareAttachmentUpdateForm, SoftwareAttachmentUploadForm, SoftwareForm
from asset.models import License, Software, SoftwareAttachment, SoftwareType
from attachment.views import AttachmentDeleteView, AttachmentUpdateView, AttachmentUploadView


class SoftwareListView(LoginRequiredMixin, ListView):
    """List view for software"""

    model = Software
    template_name = "asset/software_list.html"
    context_object_name = "software_list"
    paginate_by = 16

    def get_queryset(self):
        queryset = super().get_queryset()
        filters = {
            "q": self.request.GET.get("q"),
            "l": self.request.GET.get("l"),
            "t": self.request.GET.get("t"),
            "a": self.request.GET.get("a"),
            "show_all": self.request.GET.get("all"),
        }

        queries = {
            "q": Q(name__icontains=filters["q"]) | Q(description__icontains=filters["q"]),
            "l": Q(license_type_id=filters["l"]),
            "t": Q(software_type_id=filters["t"]),
            "a": Q(active=filters["a"]),
        }
        # Remove queries with None values
        filtered_queries = {key: query for key, query in queries.items() if filters[key]}
        for query in filtered_queries.values():
            queryset = queryset.filter(query)
        if filters["show_all"] != "true":
            queryset = queryset.exclude(active=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.get_filter_description()
        return context

    def get_filter_description(self):
        descriptions = {
            "q": ("Search Filter", self.request.GET.get("q")),
            "l": ("License", self.get_object_description(License, self.request.GET.get("l"))),
            "t": ("Software Type", self.get_object_description(SoftwareType, self.request.GET.get("t"))),
            "a": ("Active", self.request.GET.get("a")),
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


class SoftwareDetailView(LoginRequiredMixin, DetailView):
    """Detail view for software"""

    model = Software
    template_name = "asset/software_detail.html"
    context_object_name = "software"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["attachments"] = SoftwareAttachment.objects.filter(object_id=self.object.id)
        return context


class SoftwareCreateView(LoginRequiredMixin, CreateView):
    """Create view for software"""

    model = Software
    template_name = "asset/software_form.html"
    form_class = SoftwareForm
    success_url = reverse_lazy("software_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class SoftwareUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for software"""

    model = Software
    template_name = "asset/software_form.html"
    form_class = SoftwareForm
    context_object_name = "software"

    def form_valid(self, form):
        form.instance.last_updated_by = self.request.user
        next_url = self.request.POST.get("next") or self.request.GET.get("next")
        print(next_url)
        return super().form_valid(form)

    def get_success_url(self):
        """return the URL to redirect to, after processing a valid form."""

        if next_url := self.request.POST.get("next") or self.request.GET.get("next"):
            return next_url
        else:
            return reverse_lazy("software_detail", kwargs={"pk": self.object.id})


class SoftwareDeleteView(LoginRequiredMixin, DeleteView):
    """Delete view for software"""

    model = Software
    template_name = "partials/object_delete.html"
    success_url = reverse_lazy("software_list")


# Attachment views
class SoftwareAttachmentUploadView(LoginRequiredMixin, AttachmentUploadView):
    """Upload view for software attachment"""

    owner_model = Software
    form_class = SoftwareAttachmentUploadForm
    template_name = "attachment/attachment_upload_form.html"
    success_url_name = "software_detail"


class SoftwareAttachmentUpdateView(LoginRequiredMixin, AttachmentUpdateView):
    """Update view for software attachment"""

    owner_model = Software
    model = SoftwareAttachment
    form_class = SoftwareAttachmentUpdateForm
    template_name = "attachment/attachment_update_form.html"
    success_url_name = "software_detail"


class SoftwareAttachmentDeleteView(LoginRequiredMixin, AttachmentDeleteView):
    """Delete view for software attachment"""

    owner_model = Software
    model = SoftwareAttachment
    template_name = "attachment/attachment_delete_form.html"
    success_url_name = "software_detail"

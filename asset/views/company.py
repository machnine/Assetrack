"""company views"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from asset.forms import CompanyForm
from asset.models import Company


class CompanyListView(LoginRequiredMixin, ListView):
    """List view for the company model"""

    model = Company
    template_name = "asset/company_list.html"
    context_object_name = "companies"

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(notes__icontains=query))
        return queryset.order_by("name")


class CompanyCreateView(LoginRequiredMixin, CreateView):
    """Create view for the company model"""

    model = Company
    template_name = "asset/company_form.html"
    form_class = CompanyForm
    success_url = reverse_lazy("company_list")


class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for the company model"""

    model = Company
    template_name = "asset/company_form.html"
    form_class = CompanyForm
    success_url = reverse_lazy("company_list")


class CompanyDeleteView(LoginRequiredMixin, DeleteView):
    """Delete view for the company model"""

    model = Company
    template_name = "partials/object_delete.html"
    success_url = reverse_lazy("company_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse_lazy("company_list")
        return context

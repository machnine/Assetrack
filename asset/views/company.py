"""company views"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from asset.forms import CompanyForm
from asset.models import Company, SiteConfiguration


class CompanyListView(LoginRequiredMixin, ListView):
    """List view for the company model"""

    model = Company
    template_name = "asset/company_list.html"
    context_object_name = "companies"
    paginate_by = int(SiteConfiguration.get_value("PAGINATION_COMPANY_LIST") or 16)

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(notes__icontains=query))
        queryset = queryset.annotate(manufactured=Count("manufacturer", distinct=True))
        queryset = queryset.annotate(serviced=Count("service_provider", distinct=True))
        return queryset.order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q")

        if query:
            context["query"] = f"Filter: {query}"

        return context


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

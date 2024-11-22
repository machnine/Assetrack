"""category views"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from asset.forms import CategoryForm
from asset.models import Category


class CategoryListView(LoginRequiredMixin, ListView):
    """List view for the category model"""

    model = Category
    template_name = "asset/category_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(equipment_count=Count("equipment")).order_by("-equipment_count")
        return queryset

class CategoryCreateView(LoginRequiredMixin, CreateView):
    """Create view for the category model"""

    model = Category
    template_name = "asset/category_form.html"
    form_class = CategoryForm
    success_url = reverse_lazy("category_list")


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for the category model"""

    model = Category
    template_name = "asset/category_form.html"
    form_class = CategoryForm
    success_url = reverse_lazy("category_list")


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    """Delete view for the category model"""

    model = Category
    template_name = "partials/object_delete.html"
    success_url = reverse_lazy("category_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse_lazy("category_list")
        return context

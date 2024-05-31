"""category views"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from asset.models import Category


class CategoryListView(LoginRequiredMixin, ListView):
    """List view for the category model"""

    model = Category
    template_name = "asset/category_list.html"
    context_object_name = "categories"


class CategoryCreateView(LoginRequiredMixin, CreateView):
    """Create view for the category model"""

    model = Category
    template_name = "asset/category_form.html"
    fields = ["name", "description"]
    success_url = reverse_lazy("category_list")


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for the category model"""

    model = Category
    template_name = "asset/category_form.html"
    fields = ["name", "description"]
    success_url = reverse_lazy("category_list")


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    """Delete view for the category model"""

    model = Category
    template_name = "asset/category_delete.html"
    success_url = reverse_lazy("category_list")

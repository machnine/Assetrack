"""Views for the hardboiledegg app."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class HomeView(LoginRequiredMixin, TemplateView):
    """Home view"""

    template_name = "home.html"

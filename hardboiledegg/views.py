"""Views for the hardboiledegg app."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from asset.models import Equipment, Status


class HomeView(LoginRequiredMixin, TemplateView):
    """Home view"""

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        repair = Status.objects.get(name="Under Repair")
        verification = Status.objects.get(name="Pending Verification")
        context["repair_id"] = repair.id
        context["verification_id"] = verification.id
        context["under_repair"] = Equipment.objects.filter(status=repair)
        context["pending_verification"] = Equipment.objects.filter(status=verification)
        return context

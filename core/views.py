"""Views for the core app."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
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
        # replacement of equipment due in a year and not decommissioned
        one_year = timezone.now() + timezone.timedelta(days=365)
        decomissioned = Status.objects.get(name="Decommissioned")
        context["replacement_due"] = Equipment.objects.exclude(status=decomissioned).filter(
            replacement_date__lte=one_year
        )
        return context

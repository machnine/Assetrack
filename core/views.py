"""Views for the core app."""

from django.utils import timezone
from django.views.generic import TemplateView

from asset.models import Equipment, EquipmentRecord, Schedule, Status, SiteConfiguration


class HomeView(TemplateView):
    """Home view"""

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        repair = Status.objects.get(name="Under Repair")
        verification = Status.objects.get(name="Pending Verification")
        # ids of the Objects
        context["repair_id"] = repair.id
        context["verification_id"] = verification.id
        # data for the dashboard
        # schedules between today and 14 days from now
        in_two_weeks = timezone.now() + timezone.timedelta(weeks=2)
        context["schedules"] = Schedule.objects.filter(schedule_date__range=[timezone.now(), in_two_weeks], status="A")
        context["under_repair"] = Equipment.objects.filter(status=repair)
        context["pending_verification"] = Equipment.objects.filter(status=verification)
        # replacement of equipment due in a year and not decommissioned
        one_year = timezone.now() + timezone.timedelta(days=365)
        decomissioned = Status.objects.get(name="Decommissioned")
        context["replacement_due"] = Equipment.objects.exclude(status=decomissioned).filter(
            replacement_date__lte=one_year
        )
        equipment_record_display_limit = int(SiteConfiguration.get_value("LIMIT_HOME_EQUIPMENT_RECORD") or 5)
        context["equipment_records"] = EquipmentRecord.objects.filter(record_type__front_page=True).order_by("-pk")[:equipment_record_display_limit]
        return context

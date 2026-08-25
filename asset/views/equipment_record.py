"""CRUD view for equipment record"""

import csv
import re
from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from asset.forms import (
    EquipmentRecordAttachmentUpdateForm,
    EquipmentRecordAttachmentUploadForm,
    EquipmentRecordForm,
    EquipmentRecordTimelineFilterForm,
)
from asset.models import Equipment, EquipmentRecord, RecordType, SiteConfiguration
from asset.models.record import EquipmentRecordAttachment
from attachment.views import AttachmentDeleteView, AttachmentUpdateView, AttachmentUploadView


class EquipmentRecordListView(LoginRequiredMixin, ListView):
    """List view for equipment record"""

    model = EquipmentRecord
    template_name = "asset/equipmentrecord_list.html"
    context_object_name = "records"
    paginate_by = int(SiteConfiguration.get_value("PAGINATION_EQUIPMENT_RECORD") or 16)

    def get_queryset(self):
        queryset = super().get_queryset()
        filters = {"q": self.request.GET.get("q"), "record_type": self.request.GET.get("type")}

        # normalise the query string
        if filters["q"]:
            filters["q"] = re.sub(r"[^A-Za-z0-9 ]+", "", filters["q"]).strip()

        queries = {
            "q": Q(equipment__name__icontains=filters["q"]) | Q(description__icontains=filters["q"]),
            "record_type": Q(record_type=filters["record_type"]),
        }

        # Remove queries with None values
        filtered_queries = {key: query for key, query in queries.items() if filters[key]}

        for query in filtered_queries.values():
            queryset = queryset.filter(query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.get_filter_description()
        return context

    def get_filter_description(self):
        descriptions = {
            "q": ("Search Filter", self.request.GET.get("q")),
            "type": ("Record Type", self.get_object_description(RecordType, self.request.GET.get("type"))),
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


class EquipmentRecordCreateView(LoginRequiredMixin, CreateView):
    """Create view for equipment record"""

    model = EquipmentRecord
    template_name = "asset/equipmentrecord_form.html"
    form_class = EquipmentRecordForm

    def form_valid(self, form):
        # get the equipment id from the url
        form.instance.equipment_id = self.kwargs.get("equipment_id")
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("equipment_detail", kwargs={"pk": self.object.equipment.id})


class EquipmentRecordUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for equipment record"""

    model = EquipmentRecord
    template_name = "asset/equipmentrecord_form.html"
    form_class = EquipmentRecordForm
    context_object_name = "record"

    def form_valid(self, form):
        form.instance.last_updated_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("equipment_detail", kwargs={"pk": self.object.equipment.id})


class EquipmentRecordDeleteView(LoginRequiredMixin, DeleteView):
    """Delete view for equipment record"""

    model = EquipmentRecord
    template_name = "partials/object_delete.html"
    context_object_name = "record"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse_lazy("equipment_detail", kwargs={"pk": self.object.equipment.id})
        return context

    def get_success_url(self):
        return reverse_lazy("equipment_detail", kwargs={"pk": self.object.equipment.id})


class EquipmentRecordDetailView(LoginRequiredMixin, DetailView):
    """Detail view for equipment record"""

    model = EquipmentRecord
    template_name = "asset/equipmentrecord_detail.html"
    context_object_name = "record"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["attachments"] = EquipmentRecordAttachment.objects.filter(object_id=self.object.id)
        return context


class EquipmentRecordTimelineView(LoginRequiredMixin, TemplateView):
    """Plot equipment records by date, equipment, and record-type colour."""

    template_name = "asset/equipmentrecord_timeline.html"
    default_color = "#6c757d"
    color_pattern = re.compile(r"^#[0-9a-fA-F]{6}$")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            filter_form = EquipmentRecordTimelineFilterForm(self.request.GET)
            active_filters = filter_form.cleaned_data if filter_form.is_valid() else {}
        else:
            today = timezone.localdate()
            active_filters = {
                "start_date": today - relativedelta(years=3),
                "end_date": today,
                "category": None,
                "equipment": None,
                "record_type": None,
            }
            filter_form = EquipmentRecordTimelineFilterForm(initial=active_filters)

        records = EquipmentRecord.objects.select_related("equipment", "record_type")
        if active_filters.get("start_date"):
            records = records.filter(date__gte=active_filters["start_date"])
        if active_filters.get("end_date"):
            records = records.filter(date__lte=active_filters["end_date"])
        if active_filters.get("category"):
            records = records.filter(equipment__category=active_filters["category"])
        if active_filters.get("equipment"):
            records = records.filter(equipment=active_filters["equipment"])
        if active_filters.get("record_type"):
            records = records.filter(record_type=active_filters["record_type"])

        records = list(records.order_by("equipment__name", "date", "pk"))
        timeline = self.build_timeline(records, active_filters)
        context.update(
            {
                "filter_form": filter_form,
                "record_count": len(records),
                **timeline,
            }
        )
        return context

    def build_timeline(self, records, active_filters):
        if not records:
            return {"equipment_rows": [], "equipment_count": 0, "legend": [], "ticks": []}

        record_dates = [record.date for record in records]
        first_date = min(record_dates)
        last_date = max(record_dates)
        date_span = (last_date - first_date).days
        padding = max(1, round(date_span * 0.03))
        axis_start = active_filters.get("start_date") or first_date - timedelta(days=padding)
        axis_end = active_filters.get("end_date") or last_date + timedelta(days=padding)

        if axis_start == axis_end:
            axis_start -= timedelta(days=1)
            axis_end += timedelta(days=1)

        total_days = (axis_end - axis_start).days
        rows_by_equipment = {}
        record_types = {}

        for record in records:
            row = rows_by_equipment.setdefault(
                record.equipment_id,
                {"equipment": record.equipment, "events": [], "date_lanes": {}, "height": 40},
            )
            lane = row["date_lanes"].get(record.date, 0)
            row["date_lanes"][record.date] = lane + 1
            row["height"] = max(row["height"], 28 + lane * 16)
            color = self.normalise_color(record.record_type.color)
            row["events"].append(
                {
                    "record": record,
                    "color": color,
                    "position": round(((record.date - axis_start).days / total_days) * 100, 4),
                    "top": 14 + lane * 16,
                }
            )
            record_types[record.record_type_id] = {"record_type": record.record_type, "color": color}

        equipment_rows = []
        for row in rows_by_equipment.values():
            row.pop("date_lanes")
            equipment_rows.append(row)

        return {
            "axis_start": axis_start,
            "axis_end": axis_end,
            "equipment_rows": equipment_rows,
            "equipment_count": len(equipment_rows),
            "legend": sorted(record_types.values(), key=lambda item: item["record_type"].name.lower()),
            "ticks": self.build_ticks(axis_start, axis_end),
        }

    @staticmethod
    def build_ticks(axis_start, axis_end):
        total_days = (axis_end - axis_start).days
        tick_count = min(7, total_days + 1)
        label_format = "Y" if total_days > 730 else "M Y" if total_days > 90 else "d M"
        return [
            {
                "date": axis_start + timedelta(days=round((total_days * index) / (tick_count - 1))),
                "position": round((index / (tick_count - 1)) * 100, 4),
                "label_format": label_format,
            }
            for index in range(tick_count)
        ]

    def normalise_color(self, color):
        return color if color and self.color_pattern.fullmatch(color) else self.default_color


class EquipmentRecordCSVExportView(LoginRequiredMixin, View):
    """Export all records belonging to one item of equipment as CSV."""

    def get(self, request, equipment_id, *args, **kwargs):
        equipment = get_object_or_404(Equipment, pk=equipment_id)
        records = EquipmentRecord.objects.filter(equipment=equipment).select_related(
            "equipment",
            "record_type",
            "created_by",
            "last_updated_by",
        )

        filename = (
            f"assetrack_equipment_{equipment.pk}_records_"
            f"{timezone.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"
        )
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'

        csv_fields = {
            "Record ID": lambda record: record.pk,
            "Date": lambda record: record.date,
            "Record Type": lambda record: record.record_type.name,
            "Equipment": lambda record: record.equipment.name,
            "Description": lambda record: record.description or "",
            "Created At": lambda record: record.created_at,
            "Created By": lambda record: record.created_by.username if record.created_by else "",
            "Last Updated At": lambda record: record.last_updated,
            "Last Updated By": lambda record: record.last_updated_by.username if record.last_updated_by else "",
        }

        writer = csv.writer(response)
        writer.writerow(csv_fields.keys())
        for record in records:
            writer.writerow([field(record) for field in csv_fields.values()])

        return response


### EquipmentRecordAttachment CRUD operations


class EquipmentRecordAttachmentUploadView(LoginRequiredMixin, AttachmentUploadView):
    """Upload view for equipment record attachments"""

    owner_model = EquipmentRecord
    form_class = EquipmentRecordAttachmentUploadForm
    template_name = "attachment/upload_form.html"
    success_url_name = "equipmentrecord_detail"


class EquipmentRecordAttachmentUpdateView(LoginRequiredMixin, AttachmentUpdateView):
    """Update view for equipment record attachments"""

    owner_model = EquipmentRecord
    model = EquipmentRecordAttachment
    form_class = EquipmentRecordAttachmentUpdateForm
    template_name = "attachment/update_form.html"
    success_url_name = "equipmentrecord_detail"


class EquipmentRecordAttachmentDeleteView(LoginRequiredMixin, AttachmentDeleteView):
    """Delete view for equipment record attachments"""

    owner_model = EquipmentRecord
    model = EquipmentRecordAttachment
    success_url_name = "equipmentrecord_detail"
    template_name = "attachment/delete_form.html"

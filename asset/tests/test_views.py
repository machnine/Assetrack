"""Tests for asset views."""

from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from asset.models import (
    Category,
    Company,
    Equipment,
    EquipmentRecord,
    EquipmentType,
    Location,
    RecordType,
    Schedule,
    Status,
)

User = get_user_model()


class ViewTestMixin:
    """Mixin with helpers for view tests."""

    @classmethod
    def create_user(cls, username="testuser"):
        return User.objects.create_user(username=username, password="testpass123")

    @classmethod
    def create_equipment_deps(cls):
        return {
            "manufacturer": Company.objects.create(name="Acme Corp"),
            "category": Category.objects.create(name="Lab Equipment"),
            "equipment_type": EquipmentType.objects.create(name="Centrifuge"),
            "location": Location.objects.create(name="Lab A"),
            "status": Status.objects.create(name="Active"),
        }

    @classmethod
    def create_equipment(cls, user, deps, **overrides):
        defaults = {
            "name": "Test Equipment",
            "model_number": "M100",
            "serial_number": "SN001",
            "created_by": user,
            **deps,
        }
        defaults.update(overrides)
        return Equipment.objects.create(**defaults)

    def login(self):
        self.client.login(username="testuser", password="testpass123")


# ── Authentication ──────────────────────────────────────────────


class LoginRequiredTest(ViewTestMixin, TestCase):
    """Verify views redirect to login when unauthenticated."""

    def test_equipment_list_requires_login(self):
        response = self.client.get(reverse("equipment_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_equipment_record_timeline_requires_login(self):
        response = self.client.get(reverse("equipmentrecord_timeline"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_schedule_list_requires_login(self):
        response = self.client.get(reverse("schedule_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_category_list_requires_login(self):
        response = self.client.get(reverse("category_list"))
        self.assertEqual(response.status_code, 302)

    def test_location_list_requires_login(self):
        response = self.client.get(reverse("location_list"))
        self.assertEqual(response.status_code, 302)

    def test_company_list_requires_login(self):
        response = self.client.get(reverse("company_list"))
        self.assertEqual(response.status_code, 302)


# ── Equipment Views ─────────────────────────────────────────────


class EquipmentListViewTest(ViewTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()
        cls.deps = cls.create_equipment_deps()
        cls.equipment = cls.create_equipment(cls.user, cls.deps)

    def setUp(self):
        self.login()

    def test_list_renders(self):
        response = self.client.get(reverse("equipment_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Equipment")

    def test_search_filter(self):
        response = self.client.get(reverse("equipment_list"), {"q": "Test"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Equipment")

    def test_search_no_results(self):
        response = self.client.get(reverse("equipment_list"), {"q": "nonexistent"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Test Equipment")

    def test_filter_by_status(self):
        response = self.client.get(reverse("equipment_list"), {"s": self.deps["status"].id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Equipment")

    def test_decommissioned_hidden_by_default(self):
        decom = Status.objects.create(name="Decommissioned")
        Equipment.objects.create(
            name="Old Equipment",
            model_number="M200",
            serial_number="SN002",
            created_by=self.user,
            manufacturer=self.deps["manufacturer"],
            category=self.deps["category"],
            equipment_type=self.deps["equipment_type"],
            location=self.deps["location"],
            status=decom,
        )
        response = self.client.get(reverse("equipment_list"))
        self.assertNotContains(response, "Old Equipment")

    def test_show_all_includes_decommissioned(self):
        decom = Status.objects.create(name="Decommissioned")
        Equipment.objects.create(
            name="Old Equipment",
            model_number="M200",
            serial_number="SN002",
            created_by=self.user,
            manufacturer=self.deps["manufacturer"],
            category=self.deps["category"],
            equipment_type=self.deps["equipment_type"],
            location=self.deps["location"],
            status=decom,
        )
        response = self.client.get(reverse("equipment_list"), {"all": "true"})
        self.assertContains(response, "Old Equipment")


class EquipmentDetailViewTest(ViewTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()
        cls.deps = cls.create_equipment_deps()
        cls.equipment = cls.create_equipment(cls.user, cls.deps)

    def setUp(self):
        self.login()

    def test_detail_renders(self):
        response = self.client.get(reverse("equipment_detail", kwargs={"pk": self.equipment.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Equipment")
        self.assertContains(
            response,
            reverse("equipmentrecord_csv_export", kwargs={"equipment_id": self.equipment.pk}),
        )

    def test_detail_404(self):
        response = self.client.get(reverse("equipment_detail", kwargs={"pk": 9999}))
        self.assertEqual(response.status_code, 404)


class EquipmentCreateViewTest(ViewTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()
        cls.deps = cls.create_equipment_deps()

    def setUp(self):
        self.login()

    def test_create_get(self):
        response = self.client.get(reverse("equipment_create"))
        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        data = {
            "name": "New Equipment",
            "manufacturer": self.deps["manufacturer"].id,
            "model_number": "M300",
            "serial_number": "SN003",
            "category": self.deps["category"].id,
            "equipment_type": self.deps["equipment_type"].id,
            "location": self.deps["location"].id,
            "status": self.deps["status"].id,
        }
        response = self.client.post(reverse("equipment_create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Equipment.objects.filter(name="New Equipment").exists())
        eq = Equipment.objects.get(name="New Equipment")
        self.assertEqual(eq.created_by, self.user)


class EquipmentDeleteViewTest(ViewTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()
        cls.deps = cls.create_equipment_deps()

    def setUp(self):
        self.login()
        self.equipment = self.create_equipment(self.user, self.deps, serial_number="SN-DEL")

    def test_delete_post(self):
        pk = self.equipment.pk
        response = self.client.post(reverse("equipment_delete", kwargs={"pk": pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Equipment.objects.filter(pk=pk).exists())


class EquipmentCSVExportViewTest(ViewTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()
        cls.deps = cls.create_equipment_deps()
        cls.create_equipment(cls.user, cls.deps)

    def setUp(self):
        self.login()

    def test_csv_export(self):
        response = self.client.get(reverse("equipment_csv_export"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
        content = response.content.decode()
        self.assertIn("Name", content)
        self.assertIn("Test Equipment", content)


class EquipmentRecordCSVExportViewTest(ViewTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()
        cls.deps = cls.create_equipment_deps()
        cls.equipment = cls.create_equipment(cls.user, cls.deps)
        cls.other_equipment = cls.create_equipment(
            cls.user,
            cls.deps,
            name="Other Equipment",
            serial_number="SN002",
        )
        cls.record_type = RecordType.objects.create(name="Service")
        cls.record = EquipmentRecord.objects.create(
            equipment=cls.equipment,
            record_type=cls.record_type,
            date=date(2026, 8, 20),
            description="Annual service completed",
            created_by=cls.user,
        )
        EquipmentRecord.objects.create(
            equipment=cls.other_equipment,
            record_type=cls.record_type,
            date=date(2026, 8, 21),
            description="Record belonging to other equipment",
            created_by=cls.user,
        )

    def setUp(self):
        self.login()

    def test_csv_export_contains_only_selected_equipment_records(self):
        response = self.client.get(
            reverse("equipmentrecord_csv_export", kwargs={"equipment_id": self.equipment.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertIn(f"assetrack_equipment_{self.equipment.pk}_records_", response["Content-Disposition"])

        content = response.content.decode()
        self.assertIn("Record ID,Date,Record Type,Equipment,Description", content)
        self.assertIn("Annual service completed", content)
        self.assertIn("Test Equipment", content)
        self.assertNotIn("Record belonging to other equipment", content)
        self.assertNotIn("Other Equipment", content)

    def test_csv_export_404_for_invalid_equipment(self):
        response = self.client.get(reverse("equipmentrecord_csv_export", kwargs={"equipment_id": 9999}))

        self.assertEqual(response.status_code, 404)


class EquipmentRecordTimelineViewTest(ViewTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()
        cls.deps = cls.create_equipment_deps()
        cls.equipment = cls.create_equipment(cls.user, cls.deps)
        cls.other_category = Category.objects.create(name="Imaging Equipment")
        cls.other_equipment = cls.create_equipment(
            cls.user,
            cls.deps,
            name="Other Equipment",
            serial_number="SN-TIMELINE-2",
            category=cls.other_category,
        )
        cls.critical_type = RecordType.objects.create(name="Critical", color="#dc3545")
        cls.information_type = RecordType.objects.create(name="Information", color="#0dcaf0")
        cls.critical_record = EquipmentRecord.objects.create(
            equipment=cls.equipment,
            record_type=cls.critical_type,
            date=date(2026, 1, 10),
            description="Critical timeline event",
            created_by=cls.user,
        )
        cls.information_record = EquipmentRecord.objects.create(
            equipment=cls.other_equipment,
            record_type=cls.information_type,
            date=date(2026, 2, 10),
            description="Information timeline event",
            created_by=cls.user,
        )
        cls.old_record = EquipmentRecord.objects.create(
            equipment=cls.equipment,
            record_type=cls.information_type,
            date=date(2020, 6, 15),
            description="Older timeline event",
            created_by=cls.user,
        )

    def setUp(self):
        self.login()

    def test_timeline_defaults_to_the_last_three_years(self):
        response = self.client.get(reverse("equipmentrecord_timeline"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["record_count"], 2)
        self.assertEqual(response.context["equipment_count"], 2)
        today = timezone.localdate()
        self.assertEqual(response.context["filter_form"].initial["start_date"].year, today.year - 3)
        self.assertEqual(response.context["filter_form"].initial["end_date"], today)
        self.assertContains(response, "Test Equipment")
        self.assertContains(response, "Other Equipment")
        self.assertContains(response, "Critical")
        self.assertContains(response, "#dc3545")
        self.assertContains(response, reverse("equipmentrecord_detail", kwargs={"pk": self.critical_record.pk}))
        self.assertNotContains(response, "Older timeline event")

        for row in response.context["equipment_rows"]:
            for event in row["events"]:
                self.assertGreaterEqual(event["position"], 0)
                self.assertLessEqual(event["position"], 100)

    def test_timeline_can_show_records_older_than_three_years(self):
        response = self.client.get(
            reverse("equipmentrecord_timeline"),
            {"start_date": "2020-01-01", "end_date": "2020-12-31"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["record_count"], 1)
        self.assertEqual(response.context["equipment_rows"][0]["events"][0]["record"], self.old_record)

    def test_timeline_filters_by_equipment_and_record_type(self):
        response = self.client.get(
            reverse("equipmentrecord_timeline"),
            {"equipment": self.other_equipment.pk, "record_type": self.information_type.pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["record_count"], 1)
        self.assertEqual(
            [row["equipment"] for row in response.context["equipment_rows"]],
            [self.other_equipment],
        )
        self.assertEqual(
            [item["record_type"] for item in response.context["legend"]],
            [self.information_type],
        )

    def test_timeline_filters_by_equipment_category(self):
        response = self.client.get(
            reverse("equipmentrecord_timeline"),
            {
                "start_date": "2025-01-01",
                "end_date": "2026-12-31",
                "category": self.other_category.pk,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["record_count"], 1)
        self.assertEqual(
            [row["equipment"] for row in response.context["equipment_rows"]],
            [self.other_equipment],
        )

    def test_timeline_filters_by_date_range(self):
        response = self.client.get(
            reverse("equipmentrecord_timeline"),
            {"start_date": "2026-02-01", "end_date": "2026-02-28"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["record_count"], 1)
        self.assertEqual(response.context["equipment_rows"][0]["equipment"], self.other_equipment)

    def test_timeline_rejects_reversed_date_range(self):
        response = self.client.get(
            reverse("equipmentrecord_timeline"),
            {"start_date": "2026-03-01", "end_date": "2026-02-01"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["filter_form"],
            field=None,
            errors="The from date must be on or before the to date.",
        )


# ── Schedule Views ──────────────────────────────────────────────


class ScheduleListViewTest(ViewTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()

    def setUp(self):
        self.login()

    def test_list_renders(self):
        Schedule.objects.create(
            schedule_date=date.today(),
            description="Today task",
            created_by=self.user,
        )
        response = self.client.get(reverse("schedule_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Today task")

    def test_old_schedules_hidden(self):
        Schedule.objects.create(
            schedule_date=date.today() - timedelta(days=60),
            description="Old task",
            created_by=self.user,
        )
        response = self.client.get(reverse("schedule_list"))
        self.assertNotContains(response, "Old task")

    def test_completed_hidden_by_default(self):
        Schedule.objects.create(
            schedule_date=date.today(),
            description="Done task",
            status="C",
            created_by=self.user,
        )
        response = self.client.get(reverse("schedule_list"))
        self.assertNotContains(response, "Done task")

    def test_show_all_includes_completed(self):
        Schedule.objects.create(
            schedule_date=date.today(),
            description="Done task",
            status="C",
            created_by=self.user,
        )
        response = self.client.get(reverse("schedule_list"), {"all": "true"})
        self.assertContains(response, "Done task")


class ScheduleActionViewTest(ViewTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()

    def setUp(self):
        self.login()

    def test_action_one_off_completes(self):
        s = Schedule.objects.create(
            schedule_date=date.today(),
            description="One-off",
            frequency="O",
            created_by=self.user,
        )
        response = self.client.post(reverse("schedule_action", kwargs={"pk": s.pk}))
        self.assertEqual(response.status_code, 302)
        s.refresh_from_db()
        self.assertEqual(s.status, "C")

    def test_action_recurring_advances(self):
        s = Schedule.objects.create(
            schedule_date=date(2025, 6, 1),
            description="Weekly",
            frequency="W",
            created_by=self.user,
        )
        response = self.client.post(reverse("schedule_action", kwargs={"pk": s.pk}))
        s.refresh_from_db()
        self.assertEqual(s.schedule_date, date(2025, 6, 8))

    def test_action_ajax_one_off_returns_empty(self):
        s = Schedule.objects.create(
            schedule_date=date.today(),
            description="One-off",
            frequency="O",
            created_by=self.user,
        )
        response = self.client.post(
            reverse("schedule_action", kwargs={"pk": s.pk}),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"")

    def test_action_ajax_recurring_returns_html(self):
        s = Schedule.objects.create(
            schedule_date=date(2025, 6, 1),
            description="Weekly task",
            frequency="W",
            created_by=self.user,
        )
        response = self.client.post(
            reverse("schedule_action", kwargs={"pk": s.pk}),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "schedule-")

    def test_action_404_for_invalid_pk(self):
        response = self.client.post(reverse("schedule_action", kwargs={"pk": 9999}))
        self.assertEqual(response.status_code, 404)


class ScheduleCreateViewTest(ViewTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()

    def setUp(self):
        self.login()

    def test_create_get(self):
        response = self.client.get(reverse("schedule_create"))
        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        data = {
            "schedule_date": "2025-07-01",
            "description": "New schedule",
            "frequency": "O",
            "status": "A",
        }
        response = self.client.post(reverse("schedule_create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Schedule.objects.filter(description="New schedule").exists())
        s = Schedule.objects.get(description="New schedule")
        self.assertEqual(s.created_by, self.user)


# ── Lookup Table CRUD Views ────────────────────────────────────


class CategoryViewTest(ViewTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()

    def setUp(self):
        self.login()

    def test_list(self):
        Category.objects.create(name="Cat A")
        response = self.client.get(reverse("category_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cat A")

    def test_create(self):
        response = self.client.post(reverse("category_create"), {"name": "New Cat"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Category.objects.filter(name="New Cat").exists())

    def test_update(self):
        cat = Category.objects.create(name="Old Name")
        response = self.client.post(reverse("category_update", kwargs={"pk": cat.pk}), {"name": "New Name"})
        self.assertEqual(response.status_code, 302)
        cat.refresh_from_db()
        self.assertEqual(cat.name, "New Name")

    def test_delete(self):
        cat = Category.objects.create(name="To Delete")
        response = self.client.post(reverse("category_delete", kwargs={"pk": cat.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Category.objects.filter(pk=cat.pk).exists())


class LocationViewTest(ViewTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()

    def setUp(self):
        self.login()

    def test_list(self):
        Location.objects.create(name="Room 101")
        response = self.client.get(reverse("location_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Room 101")

    def test_create(self):
        response = self.client.post(reverse("location_create"), {"name": "Room 202"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Location.objects.filter(name="Room 202").exists())


class CompanyViewTest(ViewTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()

    def setUp(self):
        self.login()

    def test_list(self):
        Company.objects.create(name="Acme")
        response = self.client.get(reverse("company_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Acme")

    def test_search(self):
        Company.objects.create(name="Acme")
        Company.objects.create(name="Globex")
        response = self.client.get(reverse("company_list"), {"q": "Acme"})
        self.assertContains(response, "Acme")
        self.assertNotContains(response, "Globex")


class StatusViewTest(ViewTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()

    def setUp(self):
        self.login()

    def test_list(self):
        Status.objects.create(name="Active")
        response = self.client.get(reverse("status_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Active")

    def test_create(self):
        response = self.client.post(reverse("status_create"), {"name": "New Status"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name="New Status").exists())

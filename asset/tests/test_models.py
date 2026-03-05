"""Tests for asset models."""

from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from asset.models import (
    Calibration,
    Category,
    Company,
    Equipment,
    EquipmentType,
    Location,
    Schedule,
    SiteConfiguration,
    Status,
)

User = get_user_model()


class HelperMixin:
    """Mixin to create common test objects."""

    @classmethod
    def create_user(cls, username="testuser"):
        return User.objects.create_user(username=username, password="testpass123")

    @classmethod
    def create_equipment_deps(cls):
        """Create the required FK objects for Equipment."""
        return {
            "manufacturer": Company.objects.create(name="Acme Corp"),
            "category": Category.objects.create(name="Lab Equipment"),
            "equipment_type": EquipmentType.objects.create(name="Centrifuge"),
            "location": Location.objects.create(name="Lab A"),
            "status": Status.objects.create(name="Active"),
        }

    @classmethod
    def create_equipment(cls, user, deps=None, **overrides):
        deps = deps or cls.create_equipment_deps()
        defaults = {
            "name": "Test Equipment",
            "model_number": "M100",
            "serial_number": "SN001",
            "created_by": user,
            **deps,
        }
        defaults.update(overrides)
        return Equipment.objects.create(**defaults)


class StatusModelTest(TestCase):
    def test_str(self):
        s = Status.objects.create(name="In Service")
        self.assertEqual(str(s), "In Service")

    def test_unique_name(self):
        Status.objects.create(name="Active")
        with self.assertRaises(Exception):
            Status.objects.create(name="Active")


class CalibrationModelTest(TestCase):
    def test_str(self):
        c = Calibration.objects.create(name="UKAS")
        self.assertEqual(str(c), "UKAS")


class CategoryModelTest(TestCase):
    def test_str(self):
        c = Category.objects.create(name="Analytical")
        self.assertEqual(str(c), "Analytical")

    def test_ordering(self):
        Category.objects.create(name="Zzz")
        Category.objects.create(name="Aaa")
        names = list(Category.objects.values_list("name", flat=True))
        self.assertEqual(names, ["Aaa", "Zzz"])


class LocationModelTest(TestCase):
    def test_str(self):
        loc = Location.objects.create(name="Building 1")
        self.assertEqual(str(loc), "Building 1")


class CompanyModelTest(TestCase):
    def test_str(self):
        c = Company.objects.create(name="Acme")
        self.assertEqual(str(c), "Acme")


class EquipmentTypeModelTest(TestCase):
    def test_str(self):
        et = EquipmentType.objects.create(name="Microscope")
        self.assertEqual(str(et), "Microscope")

    def test_slug_auto_generated(self):
        et = EquipmentType.objects.create(name="Flow Cytometer")
        self.assertEqual(et.slug, "flow-cytometer")

    def test_slug_custom(self):
        et = EquipmentType.objects.create(name="Flow Cytometer", slug="flow-cyt")
        self.assertEqual(et.slug, "flow-cyt")


class EquipmentModelTest(HelperMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()
        cls.deps = cls.create_equipment_deps()
        cls.equipment = cls.create_equipment(cls.user, cls.deps)

    def test_str(self):
        self.assertEqual(str(self.equipment), "Test Equipment")

    def test_ordering(self):
        eq2 = Equipment.objects.create(
            name="Alpha Equipment",
            model_number="M200",
            serial_number="SN002",
            created_by=self.user,
            **self.deps,
        )
        names = list(Equipment.objects.values_list("name", flat=True))
        self.assertEqual(names[0], "Alpha Equipment")

    def test_has_attachment_false(self):
        self.assertFalse(self.equipment.has_attachment())


class ScheduleModelTest(HelperMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()

    def test_str(self):
        s = Schedule.objects.create(
            schedule_date=date(2025, 1, 1),
            description="Annual check",
            created_by=self.user,
        )
        self.assertIn("Annual check", str(s))

    def test_one_off_no_next_action_date(self):
        s = Schedule.objects.create(
            schedule_date=date(2025, 6, 1),
            description="One-off task",
            frequency="O",
            created_by=self.user,
        )
        self.assertIsNone(s.next_action_date)

    def test_weekly_auto_next_action_date(self):
        s = Schedule.objects.create(
            schedule_date=date(2025, 6, 1),
            description="Weekly check",
            frequency="W",
            created_by=self.user,
        )
        self.assertEqual(s.next_action_date, date(2025, 6, 8))

    def test_monthly_next_action_date(self):
        s = Schedule.objects.create(
            schedule_date=date(2025, 6, 1),
            description="Monthly check",
            frequency="M",
            created_by=self.user,
        )
        self.assertEqual(s.next_action_date, date(2025, 7, 1))

    def test_quarterly_next_action_date(self):
        s = Schedule.objects.create(
            schedule_date=date(2025, 1, 15),
            description="Quarterly",
            frequency="Q",
            created_by=self.user,
        )
        self.assertEqual(s.next_action_date, date(2025, 4, 15))

    def test_yearly_next_action_date(self):
        s = Schedule.objects.create(
            schedule_date=date(2025, 3, 1),
            description="Yearly",
            frequency="Y",
            created_by=self.user,
        )
        self.assertEqual(s.next_action_date, date(2026, 3, 1))

    def test_update_status_one_off_completes(self):
        s = Schedule.objects.create(
            schedule_date=date(2025, 6, 1),
            description="One-off",
            frequency="O",
            created_by=self.user,
        )
        s.update_scheduel_status()
        self.assertEqual(s.status, "C")

    def test_update_status_recurring_advances_date(self):
        s = Schedule.objects.create(
            schedule_date=date(2025, 6, 1),
            description="Weekly",
            frequency="W",
            created_by=self.user,
        )
        s.update_scheduel_status()
        self.assertEqual(s.schedule_date, date(2025, 6, 8))
        self.assertEqual(s.next_action_date, date(2025, 6, 15))
        self.assertEqual(s.status, "A")

    def test_update_status_cancelled_noop(self):
        s = Schedule.objects.create(
            schedule_date=date(2025, 6, 1),
            description="Cancelled",
            frequency="W",
            status="X",
            created_by=self.user,
        )
        original_date = s.schedule_date
        s.update_scheduel_status()
        self.assertEqual(s.schedule_date, original_date)
        self.assertEqual(s.status, "X")


class SiteConfigurationModelTest(TestCase):
    def test_get_value_exists(self):
        SiteConfiguration.objects.create(name="TEST_KEY", value="42")
        self.assertEqual(SiteConfiguration.get_value("TEST_KEY"), "42")

    def test_get_value_missing(self):
        self.assertIsNone(SiteConfiguration.get_value("NONEXISTENT"))

    def test_str(self):
        sc = SiteConfiguration.objects.create(name="MY_SETTING", value="val")
        self.assertEqual(str(sc), "MY_SETTING")

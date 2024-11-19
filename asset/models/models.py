"""various associated models"""

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db import models
from django.utils.text import slugify

USER = settings.AUTH_USER_MODEL


class Status(models.Model):
    """status of the asset"""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Calibration(models.Model):
    """Type of calibration required"""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class EquipmentType(models.Model):
    """type of equipment e.g. centrifuge, microscope etc."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=30, unique=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "equipment types"
        ordering = ["name"]

    def save(self, *args, **kwargs):        
        self.slug = slugify(self.slug) if self.slug else slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    """category of the asset"""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]


class Location(models.Model):
    """location of the asset"""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "locations"
        ordering = ["name"]


class Company(models.Model):
    """associated company of the asset"""

    name = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "companies"
        ordering = ["name"]


class Schedule(models.Model):
    """schedule for asset maintenance and related activities"""

    FREQUENCY_CHOICES = [
        ("O", "One-off"),
        ("D", "Daily"),
        ("W", "Weekly"),
        ("M", "Monthly"),
        ("Q", "Quarterly"),
        ("H", "Half-yearly"),
        ("Y", "Yearly"),
    ]

    STATUS_CHOICES = [
        ("A", "Active"),
        ("C", "Completed"),
        ("X", "Cancelled"),
    ]

    schedule_date = models.DateField()
    next_action_date = models.DateField(blank=True, null=True)  # for recurring schedules
    description = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="A")
    frequency = models.CharField(max_length=1, choices=FREQUENCY_CHOICES, default="O")
    created_by = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="schedules")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        USER, on_delete=models.CASCADE, related_name="updated_schedules", null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Schedule: {self.schedule_date} {self.description}"

    class Meta:
        verbose_name_plural = "schedules"
        ordering = ["schedule_date"]  # this may need some thought

    def save(self, *args, **kwargs):
        if self.frequency != "O" and not self.next_action_date:
            self.next_action_date = self.get_next_action_date()
        super().save(*args, **kwargs)

    def get_next_action_date(self):
        """calculate the next action date based on frequency"""
        if self.frequency == "D":
            return self.schedule_date + relativedelta(days=1)
        elif self.frequency == "W":
            return self.schedule_date + relativedelta(weeks=1)
        elif self.frequency == "M":
            return self.schedule_date + relativedelta(months=1)
        elif self.frequency == "Q":
            return self.schedule_date + relativedelta(months=3)
        elif self.frequency == "H":
            return self.schedule_date + relativedelta(months=6)
        elif self.frequency == "Y":
            return self.schedule_date + relativedelta(years=1)
        return self.schedule_date

    def update_scheduel_status(self):
        """update the status of the schedule after an action"""
        if self.status == "X":  # cancelled
            return

        if self.frequency == "O":
            self.status = "C"
        else:
            self.schedule_date = self.next_action_date
            self.next_action_date = self.get_next_action_date()
            self.status = "A"
        self.save()



#  model to store user modifiable site configuration
class SiteConfiguration(models.Model):
    """ model to store user modifiable site configuration """

    name = models.CharField(max_length=50, unique=True)
    value = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
    
    # static method to get the value of a configuration
    @staticmethod
    def get_value(name):
        try:
            return SiteConfiguration.objects.get(name=name).value
        except SiteConfiguration.DoesNotExist:
            return None
        
    class Meta:
        verbose_name_plural = "site configurations"
        ordering = ["name"]
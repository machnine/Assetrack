"""maintenance models"""

from django.conf import settings
from django.db import models
from django.urls import reverse

from asset.models import Equipment, EquipmentType

USER = settings.AUTH_USER_MODEL


class MaintenanceRecord(models.Model):
    """Maintenance records"""

    date = models.DateField()
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, related_name="created_by")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, related_name="updated_by")
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.date} - {self.equipment.name}"

    class Meta:
        ordering = ["-date"]
        unique_together = ["date", "equipment"]


class MaintenanceTask(models.Model):
    """maintenance tasks for Luminex machines"""

    name = models.CharField(max_length=50)
    equipment_type = models.ForeignKey(EquipmentType, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=7, default="#FFFFFF")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["equipment_type", "name"]
        unique_together = ["name", "equipment_type"]

    @property
    def get_font_color(self):
        """Returns 'black' or 'white' depending on the brightness of the background color."""
        # Strip the '#' character
        hex_color = self.color.lstrip("#")

        # Convert hex to RGB
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)

        # Calculate brightness (using the luminance formula)
        brightness = (r * 299 + g * 587 + b * 114) / 1000

        # Return white or black font color based on brightness
        return "#000000" if brightness > 128 else "#ffffff"


class MaintenanceRecordAssignment(models.Model):
    """maintenance record for Luminex machines"""

    maintenance = models.ForeignKey(MaintenanceRecord, on_delete=models.CASCADE, related_name="maintenance")
    task = models.ForeignKey(MaintenanceTask, on_delete=models.CASCADE, related_name="task")

    def __str__(self):
        return f"{self.maintenance} - {self.task}"

    class Meta:
        unique_together = ["maintenance", "task"]
        ordering = ["task", "maintenance"]


class MaintenanceRecordMenu(models.Model):
    """Maintenance records menu items"""

    equipment_type = models.ForeignKey(EquipmentType, on_delete=models.CASCADE)
    link_icon = models.CharField(max_length=50)
    link_text = models.CharField(max_length=50)

    @property
    def link_url(self):
        """Return the URL for the maintenance record list for a specific equipment type."""
        return reverse("maintenance_record_list", kwargs={"slug": self.equipment_type.slug})

    def __str__(self):
        return f"Maintenance Record menu for {self.link_text}"

    class Meta:
        ordering = ["equipment_type"]
        unique_together = ["equipment_type", "link_text"]

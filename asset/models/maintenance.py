"""maintenance models"""

from django.conf import settings
from django.db import models

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


class MaintenanceTask(models.Model):
    """maintenance tasks for Luminex machines"""

    name = models.CharField(max_length=50)
    equipment_type = models.ForeignKey(EquipmentType, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.equipment_type.name}"

    class Meta:
        ordering = ["equipment_type", "name"]


class MaintenanceRecordAssignment(models.Model):
    """maintenance record for Luminex machines"""

    maintenance = models.ForeignKey(MaintenanceRecord, on_delete=models.CASCADE, related_name="maintenance")
    task = models.ForeignKey(MaintenanceTask, on_delete=models.CASCADE, related_name="task")

    def __str__(self):
        return f"{self.maintenance} - {self.task}"

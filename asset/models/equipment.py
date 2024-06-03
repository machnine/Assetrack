"""equipment model"""

from django.db import models


class Equipment(models.Model):
    """Equipment model"""

    name = models.CharField(max_length=100)
    manufacturer = models.ForeignKey("Company", on_delete=models.PROTECT, related_name="manufacturer")
    model_number = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    inventory_number = models.CharField(max_length=100, null=True, blank=True)
    porcurement_date = models.DateField(null=True, blank=True)
    commission_date = models.DateField(null=True, blank=True)
    warranty_end = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    category = models.ForeignKey("Category", on_delete=models.PROTECT)
    location = models.ForeignKey("Location", on_delete=models.PROTECT)
    status = models.ForeignKey("Status", on_delete=models.PROTECT)
    service_provider = models.ForeignKey(
        "Company", on_delete=models.PROTECT, related_name="service_provider", blank=True, null=True
    )

    def __str__(self):
        return self.name

"""equipment model"""

from django.db import models


class Equipment(models.Model):
    name = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    porcurement_date = models.DateField(null=True, blank=True)
    commission_date = models.DateField(null=True, blank=True)
    warranty_period = models.IntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    location = models.ForeignKey('Location', on_delete=models.PROTECT)
    status = models.ForeignKey('Status', on_delete=models.PROTECT)

    def __str__(self):
        return self.name
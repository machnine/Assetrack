from django.contrib import admin

# Register your models here.
from asset.models import RecordType, Calibration

admin.site.register(RecordType)
admin.site.register(Calibration)


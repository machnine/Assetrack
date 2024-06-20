"""register models to the admin site"""

from django.contrib import admin

from asset.models import Calibration, EquipmentType, License, RecordType, SofewareType

admin.site.register(Calibration)
admin.site.register(EquipmentType)
admin.site.register(RecordType)
admin.site.register(License)
admin.site.register(SofewareType)

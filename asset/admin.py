"""register models to the admin site"""

from django.contrib import admin

from asset.models import Calibration, EquipmentType, License, RecordType, SoftwareType

admin.site.register(Calibration)
admin.site.register(RecordType)
admin.site.register(License)
admin.site.register(SoftwareType)


@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "slug")
    search_fields = ("name", "description", "slug")
    list_filter = ("name", "description", "slug")

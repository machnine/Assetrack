"""register models to the admin site"""

from django.contrib import admin

from asset.models import Calibration, EquipmentType, License, MaintenanceRecordMenu, RecordType, SoftwareType, SiteConfiguration

admin.site.register(Calibration)

@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "slug")
    search_fields = ("name", "description", "slug")
    list_filter = ("name", "description", "slug")

admin.site.register(License)

@admin.register(MaintenanceRecordMenu)
class MaintenanceRecordMenuAdmin(admin.ModelAdmin):
    list_display = ("equipment_type", "link_icon", "link_text")
    search_fields = ("equipment_type__name", "link_icon", "link_text")
    list_filter = ("equipment_type", "link_icon", "link_text")


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ("name", "value")    

admin.site.register(SoftwareType)

@admin.register(RecordType)
class RecordTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "color", "front_page")








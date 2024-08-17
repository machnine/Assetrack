"""URL Configuration for asset app"""

from django.urls import path

from asset.views import (
    category,
    company,
    equipment,
    equipment_record,
    equipment_type,
    location,
    schedule,
    software,
    software_record,
    status,
    maintenance,
)

urlpatterns = [
    path("location/", location.LocationListView.as_view(), name="location_list"),
    path("location/create/", location.LocationCreateView.as_view(), name="location_create"),
    path("location/<int:pk>/update/", location.LocationUpdateView.as_view(), name="location_update"),
    path("location/<int:pk>/delete/", location.LocationDeleteView.as_view(), name="location_delete"),
    path("company/", company.CompanyListView.as_view(), name="company_list"),
    path("company/create/", company.CompanyCreateView.as_view(), name="company_create"),
    path("company/<int:pk>/update/", company.CompanyUpdateView.as_view(), name="company_update"),
    path("company/<int:pk>/delete/", company.CompanyDeleteView.as_view(), name="company_delete"),
    path("category/", category.CategoryListView.as_view(), name="category_list"),
    path("category/create/", category.CategoryCreateView.as_view(), name="category_create"),
    path("category/<int:pk>/update/", category.CategoryUpdateView.as_view(), name="category_update"),
    path("category/<int:pk>/delete/", category.CategoryDeleteView.as_view(), name="category_delete"),
    path("status/", status.StatusListView.as_view(), name="status_list"),
    path("status/create/", status.StatusCreateView.as_view(), name="status_create"),
    path("status/<int:pk>/update/", status.StatusUpdateView.as_view(), name="status_update"),
    path("status/<int:pk>/delete/", status.StatusDeleteView.as_view(), name="status_delete"),
    # Equipment
    path("equipment/", equipment.EquipmentListView.as_view(), name="equipment_list"),
    path("equipment/create/", equipment.EquipmentCreateView.as_view(), name="equipment_create"),
    path("equipment/<int:pk>/detail/", equipment.EquipmentDetailView.as_view(), name="equipment_detail"),
    path("equipment/<int:pk>/update/", equipment.EquipmentUpdateView.as_view(), name="equipment_update"),
    path("equipment/<int:pk>/delete/", equipment.EquipmentDeleteView.as_view(), name="equipment_delete"),
    path(
        "equipment/<int:equipment_id>/record/create/",
        equipment_record.EquipmentRecordCreateView.as_view(),
        name="equipmentrecord_create",
    ),
    path(
        "equipment/record/<int:pk>/update/",
        equipment_record.EquipmentRecordUpdateView.as_view(),
        name="equipmentrecord_update",
    ),
    path(
        "equipment/record/<int:pk>/delete/",
        equipment_record.EquipmentRecordDeleteView.as_view(),
        name="equipmentrecord_delete",
    ),
    path(
        "equipment/record/<int:pk>/detail/",
        equipment_record.EquipmentRecordDetailView.as_view(),
        name="equipmentrecord_detail",
    ),
    path(
        "equipment/attachment/<int:pk>/upload/",
        equipment.EquipmentAttachmentUploadView.as_view(),
        name="equipment_attachment_upload",
    ),
    path(
        "equipment/attachment/<int:pk>/update/",
        equipment.EquipmentAttachmentUpdateView.as_view(),
        name="equipment_attachment_update",
    ),
    path(
        "equipment/attachment/<int:pk>/delete/",
        equipment.EquipmentAttachmentDeleteView.as_view(),
        name="equipment_attachment_delete",
    ),
    path(
        "equipment/record/attachment/<int:pk>/upload/",
        equipment_record.EquipmentRecordAttachmentUploadView.as_view(),
        name="equipmentrecord_attachment_upload",
    ),
    path(
        "equipment/record/attachment/<int:pk>/update/",
        equipment_record.EquipmentRecordAttachmentUpdateView.as_view(),
        name="equipmentrecord_attachment_update",
    ),
    path(
        "equipment/record/attachment/<int:pk>/delete/",
        equipment_record.EquipmentRecordAttachmentDeleteView.as_view(),
        name="equipmentrecord_attachment_delete",
    ),
    path("equipmenttype/", equipment_type.EquipmentTypeListView.as_view(), name="equipmenttype_list"),
    path("equipmenttype/create/", equipment_type.EquipmentTypeCreateView.as_view(), name="equipmenttype_create"),
    path(
        "equipmenttype/<int:pk>/update/", equipment_type.EquipmentTypeUpdateView.as_view(), name="equipmenttype_update"
    ),
    path(
        "equipmenttype/<int:pk>/delete/", equipment_type.EquipmentTypeDeleteView.as_view(), name="equipmenttype_delete"
    ),
    # Software
    path("software/", software.SoftwareListView.as_view(), name="software_list"),
    path("software/create/", software.SoftwareCreateView.as_view(), name="software_create"),
    path("software/<int:pk>/detail/", software.SoftwareDetailView.as_view(), name="software_detail"),
    path("software/<int:pk>/update/", software.SoftwareUpdateView.as_view(), name="software_update"),
    path("software/<int:pk>/delete/", software.SoftwareDeleteView.as_view(), name="software_delete"),
    path(
        "software/attachment/<int:pk>/upload/",
        software.SoftwareAttachmentUploadView.as_view(),
        name="software_attachment_upload",
    ),
    path(
        "software/attachment/<int:pk>/update/",
        software.SoftwareAttachmentUpdateView.as_view(),
        name="software_attachment_update",
    ),
    path(
        "software/attachment/<int:pk>/delete/",
        software.SoftwareAttachmentDeleteView.as_view(),
        name="software_attachment_delete",
    ),
    path(
        "software/<int:software_id>/record/create/",
        software_record.SoftwareRecordCreateView.as_view(),
        name="softwarerecord_create",
    ),
    path(
        "software/record/<int:pk>/update/",
        software_record.SoftwareRecordUpdateView.as_view(),
        name="softwarerecord_update",
    ),
    path(
        "software/record/<int:pk>/delete/",
        software_record.SoftwareRecordDeleteView.as_view(),
        name="softwarerecord_delete",
    ),
    # Schedule
    path("schedule/", schedule.ScheduleListView.as_view(), name="schedule_list"),
    path("schedule/create/", schedule.ScheduleCreateView.as_view(), name="schedule_create"),
    path("schedule/<int:pk>/update/", schedule.ScheduleUpdateView.as_view(), name="schedule_update"),
    path("schedule/<int:pk>/delete/", schedule.ScheduleDeleteView.as_view(), name="schedule_delete"),
    path("schedule/<int:pk>/action/", schedule.ScheduleActionView.as_view(), name="schedule_action"),
    # Maintenance
    path("maintenance_task/", maintenance.MaintenanceTaskListView.as_view(), name="maintenance_task_list"),
    path("maintenance_task/create/", maintenance.MaintenanceTaskCreateView.as_view(), name="maintenance_task_create"),
    path(
        "maintenance_task/<int:pk>/update/",
        maintenance.MaintenanceTaskUpdateView.as_view(),
        name="maintenance_task_update",
    ),
    path(
        "maintenance_task/<int:pk>/delete/",
        maintenance.MaintenanceTaskDeleteView.as_view(),
        name="maintenance_task_delete",
    ),
    path(
        "maintenance_record/",
        maintenance.MaintenanceRecordListView.as_view(),
        name="maintenance_record_list",
    ),
    path(
        "maintenance_record/create/",
        maintenance.MaintenanceRecordCreateView.as_view(),
        name="maintenance_record_create",
    ),
    path(
        "maintenance_record/<int:pk>/update/",
        maintenance.MaintenanceRecordUpdateView.as_view(),
        name="maintenance_record_update",
    ),
    path(
        "maintenance_record/<int:pk>/delete/",
        maintenance.MaintenanceRecordDeleteView.as_view(),
        name="maintenance_record_delete",
    ),
]

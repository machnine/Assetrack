"""URL Configuration for asset app"""

from django.urls import path

from asset.views import category, company, equipment, equipment_record, location, status

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
    path("equipment/", equipment.EquipmentListView.as_view(), name="equipment_list"),
    path("equipment/create/", equipment.EquipmentCreateView.as_view(), name="equipment_create"),
    path("equipment/<int:pk>/detail/", equipment.EquipmentDetailView.as_view(), name="equipment_detail"),
    path("equipment/<int:pk>/update/", equipment.EquipmentUpdateView.as_view(), name="equipment_update"),
    path("equipment/<int:pk>/delete/", equipment.EquipmentDeleteView.as_view(), name="equipment_delete"),
    path(
        "equipment/<int:equipment_id>/record/",
        equipment_record.EquipmentRecordListView.as_view(),
        name="equipmentrecord_list",
    ),
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
        "equipment/<int:pk>/attachment/upload/",
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
        "equipment/record/<int:pk>/attachment/upload/",
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
]

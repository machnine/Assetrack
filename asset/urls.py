"""URL Configuration for asset app"""

from django.urls import path

from asset.views import category, company, equipment, equipment_record, location, status

urlpatterns = [
    path("location/", location.LocationListView.as_view(), name="location_list"),
    path("location/create/", location.LocationCreateView.as_view(), name="location_create"),
    path("location/update/<int:pk>/", location.LocationUpdateView.as_view(), name="location_update"),
    path("location/delete/<int:pk>/", location.LocationDeleteView.as_view(), name="location_delete"),
    path("company/", company.CompanyListView.as_view(), name="company_list"),
    path("company/create/", company.CompanyCreateView.as_view(), name="company_create"),
    path("company/update/<int:pk>/", company.CompanyUpdateView.as_view(), name="company_update"),
    path("company/delete/<int:pk>/", company.CompanyDeleteView.as_view(), name="company_delete"),
    path("category/", category.CategoryListView.as_view(), name="category_list"),
    path("category/create/", category.CategoryCreateView.as_view(), name="category_create"),
    path("category/update/<int:pk>/", category.CategoryUpdateView.as_view(), name="category_update"),
    path("category/delete/<int:pk>/", category.CategoryDeleteView.as_view(), name="category_delete"),
    path("status/", status.StatusListView.as_view(), name="status_list"),
    path("status/create/", status.StatusCreateView.as_view(), name="status_create"),
    path("status/update/<int:pk>/", status.StatusUpdateView.as_view(), name="status_update"),
    path("status/delete/<int:pk>/", status.StatusDeleteView.as_view(), name="status_delete"),
    path("equipment/", equipment.EquipmentListView.as_view(), name="equipment_list"),
    path("equipment/create/", equipment.EquipmentCreateView.as_view(), name="equipment_create"),
    path("equipment/detail/<int:pk>/", equipment.EquipmentDetailView.as_view(), name="equipment_detail"),
    path("equipment/update/<int:pk>/", equipment.EquipmentUpdateView.as_view(), name="equipment_update"),
    path("equipment/delete/<int:pk>/", equipment.EquipmentDeleteView.as_view(), name="equipment_delete"),
    path(
        "equipment/<int:equipment_id>/record/",
        equipment_record.EquipmentRecordListView.as_view(),
        name="equipment_record_list",
    ),
    path(
        "equipment/<int:equipment_id>/record/create/",
        equipment_record.EquipmentRecordCreateView.as_view(),
        name="equipment_record_create",
    ),
    path(
        "equipment/record/update/<int:pk>/",
        equipment_record.EquipmentRecordUpdateView.as_view(),
        name="equipment_record_update",
    ),
    path(
        "equipment/record/delete/<int:pk>/",
        equipment_record.EquipmentRecordDeleteView.as_view(),
        name="equipment_record_delete",
    ),
]

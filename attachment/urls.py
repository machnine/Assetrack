from django.urls import path

from .views import DocumentDeleteView, DocumentListView, DocumentUpdateView, DocumentUploadView

urlpatterns = [
    path("document/upload/", DocumentUploadView.as_view(), name="document_upload"),
    path("document/update/<int:pk>/", DocumentUpdateView.as_view(), name="document_update"),
    path("document/delete/<int:pk>/", DocumentDeleteView.as_view(), name="document_delete"),
    path("document/list/", DocumentListView.as_view(), name="document_list"),
]

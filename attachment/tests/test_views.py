"""Tests for attachment/document views."""

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from attachment.models import Document

User = get_user_model()


class DocumentViewTestMixin:
    @classmethod
    def create_user(cls, username="testuser"):
        return User.objects.create_user(username=username, password="testpass123")

    def login(self):
        self.client.login(username="testuser", password="testpass123")

    def create_document(self, name="Test Doc"):
        return Document.objects.create(
            file=SimpleUploadedFile(f"{name}.pdf", b"content"),
            name=name,
            description="desc",
            uploaded_by=self.user,
        )


class DocumentListViewTest(DocumentViewTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()

    def setUp(self):
        self.login()

    def test_list_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("document_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_list_renders(self):
        doc = self.create_document()
        response = self.client.get(reverse("document_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Doc")
        doc.file.delete(save=False)

    def test_search(self):
        doc1 = self.create_document("Alpha")
        doc2 = self.create_document("Beta")
        response = self.client.get(reverse("document_list"), {"q": "Alpha"})
        self.assertContains(response, "Alpha")
        self.assertNotContains(response, "Beta")
        doc1.file.delete(save=False)
        doc2.file.delete(save=False)

    def test_search_sanitizes_special_chars(self):
        doc = self.create_document("Normal")
        response = self.client.get(reverse("document_list"), {"q": "Normal!@#$"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Normal")
        doc.file.delete(save=False)


class DocumentUploadViewTest(DocumentViewTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()

    def setUp(self):
        self.login()

    def test_upload_get(self):
        response = self.client.get(reverse("document_upload"))
        self.assertEqual(response.status_code, 200)

    def test_upload_post(self):
        f = SimpleUploadedFile("upload.pdf", b"pdf content", content_type="application/pdf")
        response = self.client.post(reverse("document_upload"), {
            "file": f,
            "name": "Uploaded Doc",
            "description": "Uploaded via test",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Document.objects.filter(name="Uploaded Doc").exists())
        Document.objects.get(name="Uploaded Doc").file.delete(save=False)

    def test_upload_no_file_fails(self):
        response = self.client.post(reverse("document_upload"), {
            "name": "No File",
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Document.objects.filter(name="No File").exists())


class DocumentUpdateViewTest(DocumentViewTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()

    def setUp(self):
        self.login()
        self.doc = self.create_document()

    def test_update_get(self):
        response = self.client.get(reverse("document_update", kwargs={"pk": self.doc.pk}))
        self.assertEqual(response.status_code, 200)

    def test_update_post(self):
        response = self.client.post(
            reverse("document_update", kwargs={"pk": self.doc.pk}),
            {"name": "Updated Name", "description": "updated"},
        )
        self.assertEqual(response.status_code, 302)
        self.doc.refresh_from_db()
        self.assertEqual(self.doc.name, "Updated Name")

    def tearDown(self):
        for doc in Document.objects.all():
            if doc.file:
                doc.file.delete(save=False)


class DocumentDeleteViewTest(DocumentViewTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user()

    def setUp(self):
        self.login()
        self.doc = self.create_document()

    def test_delete_get(self):
        response = self.client.get(reverse("document_delete", kwargs={"pk": self.doc.pk}))
        self.assertEqual(response.status_code, 200)

    def test_delete_post(self):
        pk = self.doc.pk
        response = self.client.post(reverse("document_delete", kwargs={"pk": pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Document.objects.filter(pk=pk).exists())

    def test_delete_404(self):
        response = self.client.get(reverse("document_delete", kwargs={"pk": 9999}))
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        for doc in Document.objects.all():
            if doc.file:
                doc.file.delete(save=False)

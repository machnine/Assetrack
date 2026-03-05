"""Tests for attachment models."""

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from attachment.models import Document

User = get_user_model()


class DocumentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.file = SimpleUploadedFile("testfile.pdf", b"file content", content_type="application/pdf")
        self.doc = Document.objects.create(
            file=self.file,
            name="Test Document",
            description="A test doc",
            uploaded_by=self.user,
        )

    def test_str_with_name(self):
        self.assertEqual(str(self.doc), "Test Document")

    def test_str_without_name(self):
        doc = Document.objects.create(
            file=SimpleUploadedFile("unnamed.txt", b"data"),
            uploaded_by=self.user,
        )
        self.assertIn("unnamed.txt", str(doc))

    def test_filename(self):
        self.assertEqual(self.doc.filename, "testfile.pdf")

    def test_filetype(self):
        self.assertEqual(self.doc.filetype, "pdf")

    def test_filetype_no_extension(self):
        doc = Document.objects.create(
            file=SimpleUploadedFile("noext", b"data"),
            uploaded_by=self.user,
        )
        self.assertIsNone(doc.filetype)

    def test_ordering_newest_first(self):
        doc2 = Document.objects.create(
            file=SimpleUploadedFile("second.txt", b"data"),
            name="Second",
            uploaded_by=self.user,
        )
        docs = list(Document.objects.all())
        self.assertEqual(docs[0].name, "Second")

    def tearDown(self):
        for doc in Document.objects.all():
            if doc.file:
                doc.file.delete(save=False)

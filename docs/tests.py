from django.urls import reverse
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.models import User
from docs.models import FileObject
from unittest.mock import patch


class FileAPITestCase(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(username="admin", password="Admin_123", role="admin")
        self.editor_user = User.objects.create_user(username="editor", password="editor_123", role="editor")
        self.viewer_user = User.objects.create_user(username="viewer", password="Viewer_123", role="viewer")

        self.sample_file = SimpleUploadedFile("test.txt", b"hello world", content_type="text/plain")

        self.list_create_url = reverse("file-list")
        self.detail_url_name = "file-detail"

    @patch("docs.api.v1.views.upload_file_to_minio")
    def test_admin_can_upload_file(self, mock_upload):
        mock_upload.return_value = ("unique_test.txt", "http://example.com/unique_test.txt")

        self.client.login(username="admin", password="admin123")
        response = self.client.post(self.list_create_url, {"file": self.sample_file}, format="multipart")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(FileObject.objects.count(), 1)
        file_obj = FileObject.objects.first()
        self.assertEqual(file_obj.owner, self.admin_user)
        self.assertEqual(file_obj.file_name, "unique_test.txt")
        self.assertEqual(file_obj.file_url, "http://example.com/unique_test.txt")

    @patch("docs.api.v1.views.upload_file_to_minio")
    def test_editor_can_upload_but_cannot_delete(self, mock_upload):
        mock_upload.return_value = ("unique_test.txt", "http://example.com/unique_test.txt")

        self.client.login(username="editor", password="editor123")

        response = self.client.post(self.list_create_url, {"file": self.sample_file}, format="multipart")
        self.assertEqual(response.status_code, 201)

        file_obj = FileObject.objects.first()
        detail_url = reverse(self.detail_url_name, args=[file_obj.id])

        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, 403)

    @patch("docs.api.v1.views.upload_file_to_minio")
    def test_viewer_cannot_upload_or_delete(self, mock_upload):
        self.client.login(username="viewer", password="viewer123")

        response = self.client.post(self.list_create_url, {"file": self.sample_file}, format="multipart")
        self.assertEqual(response.status_code, 403)

    @patch("docs.api.v1.views.upload_file_to_minio")
    @patch("docs.api.v1.views.delete_from_minio")
    def test_admin_can_delete_file(self, mock_delete, mock_upload):
        mock_upload.return_value = ("unique_test.txt", "http://example.com/unique_test.txt")
        mock_delete.return_value = True

        self.client.login(username="admin", password="admin123")
        response = self.client.post(self.list_create_url, {"file": self.sample_file}, format="multipart")
        file_obj = FileObject.objects.first()
        detail_url = reverse(self.detail_url_name, args=[file_obj.id])

        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(FileObject.objects.count(), 0)

    @patch("docs.api.v1.views.upload_file_to_minio")
    def test_list_files_pagination_and_filtering(self, mock_upload):
        mock_upload.return_value = ("file1.txt", "http://example.com/file1.txt")
        self.client.login(username="admin", password="admin123")

        for i in range(15):
            file = SimpleUploadedFile(f"file{i}.txt", b"content", content_type="text/plain")
            self.client.post(self.list_create_url, {"file": file}, format="multipart")
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 10)

        response = self.client.get(self.list_create_url, {"author__username": "admin"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(all([f["owner"] == self.admin_user.id for f in response.data["results"]]))

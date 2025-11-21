from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User


class UserAPITestCase(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(username="admin", password="Admin_123", role="admin")
        self.editor_user = User.objects.create_user(username="editor", password="Editor_123", role="editor")
        self.viewer_user = User.objects.create_user(username="viewer", password="Viewer_123", role="viewer")

        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.list_url = reverse("user-list")

    def test_register_user(self):
        data = {
            "username": "newuser",
            "password": "Newpassword_123",
            "email": "newuser@example.com",
            "role": "viewer"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username="newuser").exists())
        user = User.objects.get(username="newuser")
        self.assertEqual(user.role, "viewer")

    def test_login_success(self):
        response = self.client.post(self.login_url, {"username": "admin", "password": "Admin_123"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("user", response.data)
        self.assertEqual(response.data["user"]["username"], "admin")
        self.assertEqual(response.data["user"]["role"], "admin")

    def test_login_failure(self):
        response = self.client.post(self.login_url, {"username": "admin", "password": "wrongpassword"})
        self.assertEqual(response.status_code, 401)
        self.assertIn("error", response.data)

    def test_user_list_admin_can_access(self):
        self.client.login(username="admin", password="Admin_123")
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 3)

    def test_user_list_editor_cannot_access(self):
        self.client.login(username="editor", password="Editor_123")
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 403)

    def test_user_list_viewer_cannot_access(self):
        self.client.login(username="viewer", password="Viewer_123")
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 403)

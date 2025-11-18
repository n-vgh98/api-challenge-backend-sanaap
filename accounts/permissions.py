from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


class IsEditor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "editor"


class IsViewer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "viewer"


class AdminEditorCanWrite(BasePermission):
    def has_permission(self, request, view):
        if request.method in ["GET"]:
            return True

        if request.method in ["POST", "PUT", "PATCH"]:
            return request.user.role in ["admin", "editor"]

        if request.method in ["DELETE"]:
            return request.user.role == "admin"

        return False

from rest_framework import permissions


class IsProjectManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_staff or not request.user.is_authenticated:
            return False

        return request.user.is_superuser or request.user.is_staff


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

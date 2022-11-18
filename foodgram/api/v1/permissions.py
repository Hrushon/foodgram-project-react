from rest_framework import permissions


class IsAuthorOrAdminOnlyPermission(permissions.BasePermission):
    """Предоставляет доступ к изменению контента автору и администратору."""

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user or request.user.is_superuser)

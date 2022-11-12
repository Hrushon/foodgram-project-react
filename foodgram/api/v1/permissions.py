from rest_framework import permissions


class IsAuthorOnlyPermission(permissions.BasePermission):
    """Предоставляет доступ к изменению контента только автору."""

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user)

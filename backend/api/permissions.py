from rest_framework import permissions


class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    """Rights to allow everyone to read and administrators to edit."""

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and request.user.is_admin
        )


class IsAuthorOrAdminOrModeratorPermission(permissions.BasePermission):
    """Permissions allowing users and admins to edit."""

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and request.user.is_admin
            or request.user
            and request.user.is_authenticated
            or obj.author == request.user
        )

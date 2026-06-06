# users_auth_app/api/permissions.py

from rest_framework import permissions


class IsProfileOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow authenticated users to read profiles.

    Only the profile owner is allowed to update the profile.
    """

    def has_object_permission(self, request, view, obj):
        """Return whether the request user may access or modify the object."""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user

from rest_framework import permissions


class IsBusinessUserOrReadOnly(permissions.BasePermission):
    """Allow everyone to read offers, but only business users to create them."""

    def has_permission(self, request, view):
        """Return whether the user may access the requested action."""
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "type", None) == "business"
        )


class IsOfferOwnerOrReadOnly(permissions.BasePermission):
    """Allow authenticated users to read offers and only owners to update them."""

    def has_object_permission(self, request, view, obj):  # type:ignore
        """Return whether the user may access or modify the offer."""
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)

        return obj.business_user == request.user

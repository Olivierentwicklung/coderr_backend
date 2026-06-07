from rest_framework.permissions import BasePermission


class IsCustomerUser(BasePermission):
    """Allow access only to authenticated users with type customer."""

    message = "Only customer users can create orders."

    def has_permission(self, request, view):  # type:ignore
        """Return whether the current user is a customer user."""
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.type == "customer"
        )


class IsBusinessUser(BasePermission):
    """Allow access only to authenticated business users."""

    message = "Only business users can update orders."

    def has_permission(self, request, view):  # type:ignore
        """Return whether the current user is an authenticated business user."""
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.type == "business"
        )

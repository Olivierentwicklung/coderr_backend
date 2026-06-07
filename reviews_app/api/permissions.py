from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthenticatedCustomerOrReadOnly(BasePermission):
    """Allow all authenticated users to read, but only customers to create reviews."""

    def has_permission(self, request, view):  # type:ignore
        """Return whether the current user may access the review endpoint."""
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        return request.user.type == "customer"

from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthenticatedCustomerOrReadOnly(BasePermission):
    """Allow authenticated users to read reviews, but only customers to create them."""

    def has_permission(self, request, view):  # type:ignore
        """Return whether the user may access the reviews endpoint."""
        if not request.user or not request.user.is_authenticated:
            return False

        return request.method in SAFE_METHODS or request.user.type == "customer"


class IsReviewOwner(BasePermission):
    """Allow only the review creator to update a review."""

    def has_object_permission(self, request, view, obj):
        """Return whether the current user owns the review."""
        return obj.reviewer == request.user

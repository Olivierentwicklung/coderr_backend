from django.db import OperationalError
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, status
from rest_framework.response import Response

from reviews_app.api.permissions import IsAuthenticatedCustomerOrReadOnly, IsReviewOwner
from reviews_app.api.serializers import ReviewSerializer
from reviews_app.models import Review

from .schema.base_schema import REVIEWS_TAG
from .schema.reviews_create_schema import REVIEWS_CREATE_DESCRIPTION
from .schema.reviews_list_schema import REVIEWS_LIST_DESCRIPTION


@extend_schema(tags=REVIEWS_TAG)
@extend_schema_view(
    get=extend_schema(
        description=REVIEWS_LIST_DESCRIPTION,
    ),
    post=extend_schema(description=REVIEWS_CREATE_DESCRIPTION),
)
class ReviewListCreateView(generics.ListCreateAPIView):
    """List reviews and allow authenticated customers to create reviews."""

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedCustomerOrReadOnly]

    def get_queryset(self):  # type:ignore
        """Return reviews filtered by business user, reviewer, and ordering."""
        queryset = Review.objects.all()

        business_user_id = self.request.query_params.get("business_user_id")  # type:ignore
        reviewer_id = self.request.query_params.get("reviewer_id")  # type:ignore
        ordering = self.request.query_params.get("ordering")  # type:ignore

        if business_user_id:
            queryset = queryset.filter(business_user_id=business_user_id)

        if reviewer_id:
            queryset = queryset.filter(reviewer_id=reviewer_id)

        if ordering in ["updated_at", "rating"]:
            queryset = queryset.order_by(ordering)

        return queryset

    def list(self, request, *args, **kwargs):
        """Return reviews or 500 if an unexpected database error occurs."""
        try:
            return super().list(request, *args, **kwargs)
        except OperationalError:
            return Response(
                {"detail": "Internal server error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def perform_create(self, serializer):
        """Save the authenticated user as the review creator."""
        serializer.save(reviewer=self.request.user)


@extend_schema(tags=REVIEWS_TAG)
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete review instances."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewOwner]

    http_method_names = ["patch", "delete"]

    def patch(self, request, *args, **kwargs):
        """Partially update rating and description for the review owner."""
        try:
            return self.partial_update(request, *args, **kwargs)
        except OperationalError:
            return Response(
                {"detail": "Internal server error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, *args, **kwargs):
        """Delete a review when the authenticated user is the owner."""
        return self.destroy(request, *args, **kwargs)

from django.db import OperationalError
from rest_framework import generics, status
from rest_framework.response import Response

from reviews_app.api.permissions import IsAuthenticatedCustomerOrReadOnly
from reviews_app.api.serializers import ReviewSerializer
from reviews_app.models import Review


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

    def create(self, request, *args, **kwargs):
        """Create a review or return 500 for unexpected database errors."""
        try:
            return super().create(request, *args, **kwargs)
        except OperationalError:
            return Response(
                {"detail": "Internal server error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

from django.db import OperationalError
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from reviews_app.api.serializers import ReviewSerializer
from reviews_app.models import Review


class ReviewListView(generics.ListAPIView):
    """List reviews for authenticated users with filtering and ordering support."""

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):  # type:ignore
        """Return reviews filtered by business user, reviewer, and allowed ordering."""
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
        """Return reviews or a 500 response when an unexpected database error occurs."""
        try:
            return super().list(request, *args, **kwargs)
        except OperationalError:
            return Response(
                {"detail": "Internal server error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

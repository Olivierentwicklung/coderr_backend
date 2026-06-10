from decimal import ROUND_HALF_UP, Decimal

from django.contrib.auth import get_user_model
from django.db.models import Avg
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from offers_app.models import Offer
from reviews_app.models import Review

User = get_user_model()


@extend_schema(tags=["Übergreifende Endpoints"])
class BaseInfoView(APIView):
    """Return public platform-wide base statistics."""

    permission_classes = [AllowAny]

    def get(self, request):
        """Return review, rating, business profile, and offer statistics."""
        try:
            review_count = Review.objects.count()
            average_rating = Review.objects.aggregate(avg_rating=Avg("rating"))[
                "avg_rating"
            ]
            business_profile_count = User.objects.filter(type="business").count()
            offer_count = Offer.objects.count()

            return Response(
                {
                    "review_count": review_count,
                    "average_rating": self._format_average_rating(average_rating),
                    "business_profile_count": business_profile_count,
                    "offer_count": offer_count,
                },
                status=status.HTTP_200_OK,
            )

        except Exception:
            return Response(
                {"detail": "Internal server error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def _format_average_rating(self, average_rating):
        """Return the average rating rounded to one decimal place."""
        if average_rating is None:
            return 0.0

        return float(
            Decimal(str(average_rating)).quantize(
                Decimal("0.1"),
                rounding=ROUND_HALF_UP,
            )
        )

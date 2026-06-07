from django.db.models import Min, Q
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from offers_app.api.pagination import OfferPagination
from offers_app.api.serializers import OfferListSerializer
from offers_app.models import Offer


class OfferListView(generics.ListAPIView):
    """API view for listing offers."""

    serializer_class = OfferListSerializer
    pagination_class = OfferPagination
    permission_classes = [AllowAny]

    allowed_ordering_fields = {
        "updated_at",
        "-updated_at",
        "min_price",
        "-min_price",
    }

    def get_queryset(self):  # type:ignore
        """Return optimized, filtered, searched, and ordered offers."""
        queryset = (
            Offer.objects.select_related("business_user")
            .prefetch_related("details")
            .annotate(
                annotated_min_price=Min("details__price"),
                annotated_min_delivery_time=Min("details__delivery_time_in_days"),
            )
        )

        params = self.request.query_params  # type:ignore

        queryset = self._filter_by_creator(queryset, params)
        queryset = self._filter_by_min_price(queryset, params)
        queryset = self._filter_by_max_delivery_time(queryset, params)
        queryset = self._filter_by_search(queryset, params)

        return self._apply_ordering(queryset, params)

    def list(self, request, *args, **kwargs):
        """Return paginated offers or a 500 response for unexpected errors."""
        try:
            return super().list(request, *args, **kwargs)
        except ValidationError:
            raise
        except Exception:
            return Response(
                {"detail": "Internal server error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def _filter_by_creator(self, queryset, params):
        """Filter offers by creator ID."""
        creator_id = params.get("creator_id")

        if creator_id is None:
            return queryset

        try:
            creator_id = int(creator_id)
        except ValueError as exc:
            raise ValidationError({"creator_id": "Must be a valid integer."}) from exc

        return queryset.filter(business_user_id=creator_id)

    def _filter_by_min_price(self, queryset, params):
        """Filter offers by minimum price."""
        min_price = params.get("min_price")

        if min_price is None:
            return queryset

        try:
            min_price = float(min_price)
        except ValueError as exc:
            raise ValidationError({"min_price": "Must be a valid number."}) from exc

        return queryset.filter(annotated_min_price__gte=min_price)

    def _filter_by_max_delivery_time(self, queryset, params):
        """Filter offers by maximum delivery time."""
        max_delivery_time = params.get("max_delivery_time")

        if max_delivery_time is None:
            return queryset

        try:
            max_delivery_time = int(max_delivery_time)
        except ValueError as exc:
            raise ValidationError(
                {"max_delivery_time": "Must be a valid integer."}
            ) from exc

        return queryset.filter(
            annotated_min_delivery_time__lte=max_delivery_time,
        )

    def _filter_by_search(self, queryset, params):
        """Search offers by title and description."""
        search = params.get("search")

        if not search:
            return queryset

        return queryset.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )

    def _apply_ordering(self, queryset, params):
        """Apply ordering by updated_at or min_price."""
        ordering = params.get("ordering")

        if not ordering:
            return queryset.order_by("id")

        if ordering == "updated_at":
            return queryset.order_by("updated_at")

        if ordering == "-updated_at":
            return queryset.order_by("-updated_at")

        if ordering == "min_price":
            return queryset.order_by("annotated_min_price")

        if ordering == "-min_price":
            return queryset.order_by("-annotated_min_price")

        raise ValidationError({"ordering": "Invalid ordering field."})

from django.db.models import Min
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny

from offers_app.api.filters import OfferFilter
from offers_app.api.pagination import OfferPagination
from offers_app.api.serializers import OfferListSerializer
from offers_app.models import Offer


class OfferListView(generics.ListAPIView):
    """API view for listing offers."""

    serializer_class = OfferListSerializer
    pagination_class = OfferPagination
    permission_classes = [AllowAny]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = OfferFilter
    search_fields = ["title", "description"]

    def get_queryset(self):  # type:ignore
        """Return optimized offer queryset."""
        return (
            Offer.objects.select_related("business_user")
            .prefetch_related("details")
            .annotate(
                annotated_min_price=Min("details__price"),
                annotated_min_delivery_time=Min("details__delivery_time_in_days"),
            )
        )

    def filter_queryset(self, queryset):
        """Apply default filters and custom ordering."""
        queryset = super().filter_queryset(queryset)
        return self._apply_ordering(queryset, self.request.query_params)  # type:ignore

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

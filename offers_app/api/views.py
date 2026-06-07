from django.db.models import Min
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.exceptions import ValidationError

from offers_app.api.filters import OfferFilter
from offers_app.api.pagination import OfferPagination
from offers_app.api.permissions import IsBusinessUserOrReadOnly
from offers_app.api.serializers import OfferCreateSerializer, OfferListSerializer
from offers_app.models import Offer


class OfferListCreateView(generics.ListCreateAPIView):
    """API view for listing and creating offers."""

    pagination_class = OfferPagination
    permission_classes = [IsBusinessUserOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = OfferFilter
    search_fields = ["title", "description"]

    def get_serializer_class(self):  # type:ignore
        """Return the serializer class based on the request method."""
        if self.request.method == "POST":
            return OfferCreateSerializer

        return OfferListSerializer

    def get_queryset(self):  # type:ignore
        """Return optimized offer queryset with price and delivery annotations."""
        return (
            Offer.objects.select_related("business_user")
            .prefetch_related("details")
            .annotate(
                annotated_min_price=Min("details__price"),
                annotated_min_delivery_time=Min("details__delivery_time_in_days"),
            )
        )

    def filter_queryset(self, queryset):
        """Apply filtering, search, and custom ordering to the queryset."""
        queryset = super().filter_queryset(queryset)

        if self.request.method == "GET":
            return self._apply_ordering(queryset, self.request.query_params)  # type:ignore

        return queryset

    def list(self, request, *args, **kwargs):
        """Return paginated offers or a 500 response for unexpected errors."""
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Create an offer."""
        return super().create(request, *args, **kwargs)

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

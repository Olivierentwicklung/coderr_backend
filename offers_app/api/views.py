from django.db.models import Min, Prefetch
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from offers_app.api.filters import OfferFilter
from offers_app.api.pagination import OfferPagination
from offers_app.api.permissions import IsBusinessUserOrReadOnly
from offers_app.api.serializers import (
    OfferCreateSerializer,
    OfferListSerializer,
    OfferRetrieveSerializer,
)
from offers_app.models import Offer, OfferDetail


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
        """Return optimized, ordered offer queryset."""
        queryset = (
            Offer.objects.select_related("business_user")
            .prefetch_related("details")
            .annotate(
                annotated_min_price=Min("details__price"),
                annotated_min_delivery_time=Min("details__delivery_time_in_days"),
            )
        )

        return self._apply_ordering(queryset, self.request.query_params)  # type:ignore

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


class OfferRetrieveView(generics.RetrieveAPIView):
    """API view for retrieving a single offer."""

    serializer_class = OfferRetrieveSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # type:ignore
        """Return optimized queryset for retrieving offers."""
        return Offer.objects.prefetch_related(
            Prefetch(
                "details",
                queryset=OfferDetail.objects.prefetch_related("features"),
            )
        )

    def retrieve(self, request, *args, **kwargs):
        """Return a single offer or a 500 response for unexpected errors."""
        try:
            return super().retrieve(request, *args, **kwargs)
        except Http404:
            raise
        except Exception:
            return Response(
                {"detail": "Internal server error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

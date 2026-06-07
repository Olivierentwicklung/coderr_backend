from django.db.models import Min, Prefetch
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response

from offers_app.api.filters import OfferFilter
from offers_app.api.pagination import OfferPagination
from offers_app.api.permissions import IsBusinessUserOrReadOnly, IsOfferOwnerOrReadOnly
from offers_app.api.serializers import (
    OfferCreateSerializer,
    OfferDetailSerializer,
    OfferListSerializer,
    OfferRetrieveSerializer,
    OfferUpdateSerializer,
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


class OfferRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """API view for retrieving, updating, and deleting a single offer."""

    permission_classes = [
        permissions.IsAuthenticated,
        IsOfferOwnerOrReadOnly,
    ]
    http_method_names = ["get", "patch", "delete", "head", "options"]

    def get_serializer_class(self):  # type:ignore
        """Return serializer class depending on request method."""
        if self.request.method == "PATCH":
            return OfferUpdateSerializer

        return OfferRetrieveSerializer

    def get_queryset(self):  # type:ignore
        """Return optimized queryset for retrieve and update operations."""
        return Offer.objects.select_related("business_user").prefetch_related(
            Prefetch(
                "details",
                queryset=OfferDetail.objects.prefetch_related("features").order_by(
                    "id"
                ),
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

    def partial_update(self, request, *args, **kwargs):
        """Partially update an offer."""
        try:
            return super().partial_update(request, *args, **kwargs)
        except Http404:
            raise
        except APIException:
            raise
        except Exception:
            return Response(
                {"detail": "Internal server error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, *args, **kwargs):
        """Delete an offer or return 500 for unexpected errors."""
        try:
            return super().destroy(request, *args, **kwargs)
        except Http404:
            raise
        except APIException:
            raise
        except Exception:
            return Response(
                {"detail": "Internal server error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class OfferDetailRetrieveView(generics.RetrieveAPIView):
    """API view for retrieving a single offer detail."""

    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # type:ignore
        """Return optimized offer detail queryset with related features."""
        return OfferDetail.objects.prefetch_related("features")

    def retrieve(self, request, *args, **kwargs):
        """Return an offer detail or a 500 response for unexpected errors."""
        try:
            return super().retrieve(request, *args, **kwargs)
        except Http404:
            raise
        except APIException:
            raise
        except Exception:
            return Response(
                {"detail": "Internal server error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

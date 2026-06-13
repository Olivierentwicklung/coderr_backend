from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from offers_app.models import OfferDetail
from orders_app.api.permissions import IsBusinessUser, IsCustomerUser
from orders_app.api.serializers import OrderSerializer, OrderStatusUpdateSerializer
from orders_app.models import Order

from .schema.base_schema import ORDERS_TAG
from .schema.orders_create_schema import ORDERS_CREATE_DESCRIPTION
from .schema.orders_delete_by_id_schema import ORDERS_DELETE_BY_ID_DESCRIPTION
from .schema.orders_list_schema import ORDERS_LIST_DESCRIPTION
from .schema.orders_partial_update_by_id_schema import (
    ORDERS_PARTIAL_UPDATE_BY_ID_DESCRIPTION,
)

User = get_user_model()


@extend_schema(tags=ORDERS_TAG)
@extend_schema_view(
    get=extend_schema(
        description=ORDERS_LIST_DESCRIPTION,
    ),
    post=extend_schema(description=ORDERS_CREATE_DESCRIPTION),
)
class OrderListCreateView(generics.ListCreateAPIView):
    """List related orders or create a new order from an offer detail."""

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):  # type:ignore
        """Return orders where the authenticated user is customer or business."""
        user = self.request.user

        return (
            Order.objects.filter(Q(customer_user=user) | Q(business_user=user))
            .select_related(
                "customer_user", "business_user", "offer_detail", "offer_detail__offer"
            )
            .prefetch_related("offer_detail__features")
            .order_by("id")
        )

    def get_permissions(self):
        """Return method-specific permissions."""
        if self.request.method == "POST":
            return [IsAuthenticated(), IsCustomerUser()]

        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        """Create an order and return the full order representation."""
        offer_detail_id = request.data.get("offer_detail_id")

        if offer_detail_id in [None, ""]:
            return Response(
                {"offer_detail_id": ["This field is required."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            offer_detail_id = int(offer_detail_id)
        except (TypeError, ValueError):
            return Response(
                {"offer_detail_id": ["A valid integer is required."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        offer_detail = get_object_or_404(
            OfferDetail.objects.select_related("offer").prefetch_related("features"),
            pk=offer_detail_id,
        )

        order = Order.objects.create(
            customer_user=request.user,
            business_user=offer_detail.offer.business_user,
            offer_detail=offer_detail,
            status="in_progress",
        )

        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=ORDERS_TAG)
@extend_schema_view(
    patch=extend_schema(
        description=ORDERS_PARTIAL_UPDATE_BY_ID_DESCRIPTION,
    ),
    delete=extend_schema(description=ORDERS_DELETE_BY_ID_DESCRIPTION),
)
class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Update or delete a single order."""

    queryset = (
        Order.objects.select_related(
            "customer_user",
            "business_user",
            "offer_detail",
            "offer_detail__offer",
        )
        .prefetch_related("offer_detail__features")
        .order_by("id")
    )
    serializer_class = OrderStatusUpdateSerializer
    http_method_names = ["patch", "delete"]

    def get_permissions(self):
        """Return method-specific permissions for order detail actions."""
        if self.request.method == "DELETE":
            return [IsAuthenticated(), IsAdminUser()]

        return [IsAuthenticated(), IsBusinessUser()]

    def get_object(self):
        try:
            order = self.get_queryset().get(pk=self.kwargs["pk"])
        except Order.DoesNotExist:
            raise NotFound("The specified order was not found.")

        if self.request.method == "PATCH" and order.business_user != self.request.user:
            raise PermissionDenied("You do not have permission to update this order.")

        return order

    def partial_update(self, request, *args, **kwargs):
        """Update the order status and return the full order representation."""
        order = self.get_object()

        serializer = self.get_serializer(
            order,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """Delete an order and return no response body."""
        order = self.get_object()
        order.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=ORDERS_TAG)
class OrderCountView(APIView):
    """Return the number of in-progress orders for a business user."""

    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        """Return the count of running orders for the given business user."""
        business_user = User.objects.filter(
            pk=business_user_id,
            type="business",
        ).first()

        if business_user is None:
            return Response(
                {"detail": "Business user not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        order_count = Order.objects.filter(
            business_user=business_user,
            status="in_progress",
        ).count()

        return Response(
            {"order_count": order_count},
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=ORDERS_TAG)
class CompletedOrderCountView(APIView):
    """Return the number of completed orders for a business user."""

    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        """Return the count of completed orders for the given business user."""
        business_user = User.objects.filter(
            pk=business_user_id,
            type="business",
        ).first()

        if business_user is None:
            return Response(
                {"detail": "Business user not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        completed_order_count = Order.objects.filter(
            business_user=business_user,
            status="completed",
        ).count()

        return Response(
            {"completed_order_count": completed_order_count},
            status=status.HTTP_200_OK,
        )

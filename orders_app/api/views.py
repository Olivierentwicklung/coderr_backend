from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from offers_app.models import OfferDetail
from orders_app.api.permissions import IsCustomerUser
from orders_app.api.serializers import OrderCreateSerializer, OrderSerializer
from orders_app.models import Order


class OrderListCreateView(generics.ListCreateAPIView):
    """List related orders or create a new order from an offer detail."""

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

    def get_serializer_class(self):  # type:ignore
        """Return the serializer class for the current request method."""
        if self.request.method == "POST":
            return OrderCreateSerializer

        return OrderSerializer

    def create(self, request, *args, **kwargs):
        """Create an order and return the full order representation."""
        offer_detail_id = request.data.get("offer_detail_id")

        if offer_detail_id in [None, ""]:
            return Response(
                {"offer_detail_id": ["This field is required."]},
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

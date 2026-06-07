from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from orders_app.api.serializers import OrderSerializer
from orders_app.models import Order


class OrderListView(generics.ListAPIView):
    """List orders related to the authenticated user."""

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):  # type:ignore
        """Return orders where the authenticated user is customer or business."""
        user = self.request.user

        return (
            Order.objects.filter(Q(customer_user=user) | Q(business_user=user))
            .select_related(
                "customer_user",
                "business_user",
                "offer_detail",
            )
            .prefetch_related("offer_detail__features")
            .order_by("id")
        )

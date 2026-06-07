from rest_framework import serializers

from offers_app.models import OfferDetail
from orders_app.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """Serialize orders with flattened offer detail data."""

    title = serializers.CharField(source="offer_detail.title", read_only=True)
    revisions = serializers.IntegerField(
        source="offer_detail.revisions", read_only=True
    )
    delivery_time_in_days = serializers.IntegerField(
        source="offer_detail.delivery_time_in_days",
        read_only=True,
    )
    price = serializers.IntegerField(source="offer_detail.price", read_only=True)
    offer_type = serializers.CharField(source="offer_detail.offer_type", read_only=True)
    features = serializers.SerializerMethodField()

    class Meta:
        """Define fields returned by the order list endpoint."""

        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        ]

    def get_features(self, obj):
        """Return all feature descriptions from the related offer detail."""
        return [feature.description for feature in obj.offer_detail.features.all()]


class OrderCreateSerializer(serializers.Serializer):
    """Validate order creation input and create an order from an offer detail."""

    offer_detail_id = serializers.IntegerField(required=True)

    def validate_offer_detail_id(self, value):
        """Validate that the referenced offer detail exists."""
        try:
            self.offer_detail = OfferDetail.objects.select_related("offer").get(
                pk=value
            )
        except OfferDetail.DoesNotExist:
            raise serializers.ValidationError("Invalid offer_detail_id.")

        return value

    def create(self, validated_data):
        """Create an order using the authenticated customer and offer detail."""
        request = self.context["request"]
        offer_detail = self.offer_detail

        return Order.objects.create(
            customer_user=request.user,
            business_user=offer_detail.offer.business_user,
            offer_detail=offer_detail,
            status="in_progress",
        )

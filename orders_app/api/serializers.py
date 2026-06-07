from rest_framework import serializers

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

from rest_framework import serializers

from offers_app.models import Offer, OfferDetail


class OfferDetailLinkSerializer(serializers.ModelSerializer):
    """Serializer for compact offer detail links."""

    url = serializers.SerializerMethodField()

    class Meta:
        """Meta configuration for offer detail links."""

        model = OfferDetail
        fields = ["id", "url"]

    def get_url(self, obj):
        """Return the relative offer detail URL."""
        return f"/offerdetails/{obj.id}/"


class OfferListSerializer(serializers.ModelSerializer):
    """Serializer for listing offers."""

    user = serializers.IntegerField(source="business_user.id", read_only=True)
    details = OfferDetailLinkSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        """Meta configuration for offer list serializer."""

        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
            "user_details",
        ]

    def get_min_price(self, obj):
        """Return the lowest detail price of the offer."""
        return (
            getattr(obj, "annotated_min_price", None)
            or obj.details.order_by("price").values_list("price", flat=True).first()
        )

    def get_min_delivery_time(self, obj):
        """Return the shortest delivery time of the offer."""
        return (
            getattr(obj, "annotated_min_delivery_time", None)
            or obj.details.order_by("delivery_time_in_days")
            .values_list("delivery_time_in_days", flat=True)
            .first()
        )

    def get_user_details(self, obj):
        """Return public business user details."""
        return {
            "first_name": obj.business_user.first_name,
            "last_name": obj.business_user.last_name,
            "username": obj.business_user.username,
        }

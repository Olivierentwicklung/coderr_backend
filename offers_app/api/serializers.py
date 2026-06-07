from django.db import transaction
from rest_framework import serializers

from offers_app.models import Offer, OfferDetail, OfferDetailFeature
from uploads_app.models import FileUpload


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


class OfferDetailCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating offer details with features."""

    features = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False,
        write_only=True,
    )

    class Meta:
        model = OfferDetail
        fields = [
            "id",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]
        read_only_fields = ["id"]

    def to_representation(self, instance):
        """Return offer detail with features as a list of strings."""
        representation = super().to_representation(instance)
        representation["features"] = list(
            instance.features.values_list("description", flat=True)
        )
        return representation


class OfferCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating offers with exactly three details."""

    image = serializers.PrimaryKeyRelatedField(
        queryset=FileUpload.objects.all(),
        required=False,
        allow_null=True,
    )
    details = OfferDetailCreateSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            "id",
            "title",
            "image",
            "description",
            "details",
        ]
        read_only_fields = ["id"]

    def validate_details(self, details):
        """Validate that an offer contains exactly three details."""
        if len(details) != 3:
            raise serializers.ValidationError(
                "An offer must contain exactly three details."
            )
        return details

    @transaction.atomic
    def create(self, validated_data):
        """Create an offer with nested details and features."""
        details_data = validated_data.pop("details")
        user = self.context["request"].user

        offer = Offer.objects.create(
            business_user=user,
            **validated_data,
        )

        for detail_data in details_data:
            features = detail_data.pop("features")

            offer_detail = OfferDetail.objects.create(
                offer=offer,
                **detail_data,
            )

            OfferDetailFeature.objects.bulk_create(
                OfferDetailFeature(
                    offer_detail=offer_detail,
                    description=feature,
                )
                for feature in features
            )

        return offer

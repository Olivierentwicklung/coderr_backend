from django.db import transaction
from rest_framework import serializers

from offers_app.models import Offer, OfferDetail, OfferDetailFeature
from uploads_app.models import FileUpload


class OfferDetailLinkSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for compact offer detail links."""

    class Meta:
        """Meta configuration for offer detail links."""

        model = OfferDetail
        fields = ["id", "url"]


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


class OfferDetailSerializer(serializers.ModelSerializer):
    """Serializer for returning offer detail data with feature strings."""

    features = serializers.SerializerMethodField()

    class Meta:
        """Meta configuration for offer detail serializer."""

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

    def get_features(self, obj):
        """Return all feature descriptions as a list of strings."""
        return list(obj.features.values_list("description", flat=True))


class OfferRetrieveSerializer(serializers.ModelSerializer):
    """Serializer for retrieving a single offer with all details."""

    user = serializers.IntegerField(source="business_user.id", read_only=True)
    details = OfferDetailLinkSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        """Meta configuration for offer retrieve serializer."""

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


class OfferDetailUpdateSerializer(serializers.Serializer):
    """Serializer for partially updating a single offer detail."""

    title = serializers.CharField(required=False)
    revisions = serializers.IntegerField(required=False, min_value=0)
    delivery_time_in_days = serializers.IntegerField(required=False, min_value=1)
    price = serializers.IntegerField(required=False, min_value=0)
    features = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=False,
    )
    offer_type = serializers.ChoiceField(
        choices=OfferDetail.OFFER_TYPE_CHOICES,
        required=True,
    )


class OfferUpdateSerializer(serializers.ModelSerializer):
    """Serializer for partially updating offers and nested details."""

    details = OfferDetailUpdateSerializer(many=True, required=False)

    class Meta:
        """Meta configuration for offer update serializer."""

        model = Offer
        fields = [
            "title",
            "image",
            "description",
            "details",
        ]

    def validate_details(self, value):
        """Validate submitted detail updates."""
        offer_types = []

        for index, detail in enumerate(value):
            offer_type = detail.get("offer_type")

            if not offer_type:
                raise serializers.ValidationError(
                    {index: {"offer_type": "This field is required."}}
                )

            offer_types.append(offer_type)

        if len(offer_types) != len(set(offer_types)):
            raise serializers.ValidationError(
                "Each offer_type may only be provided once."
            )

        return value

    @transaction.atomic
    def update(self, instance, validated_data):
        """Update an offer and only the submitted nested details."""
        details_data = validated_data.pop("details", None)

        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()

        if details_data is not None:
            self._update_details(instance, details_data)

        return instance

    def _update_details(self, offer, details_data):
        """Update matching offer details by offer_type."""
        existing_details = {
            detail.offer_type: detail
            for detail in offer.details.prefetch_related("features")
        }

        for index, detail_data in enumerate(details_data):
            offer_type = detail_data.pop("offer_type", None)

            if not offer_type:
                raise serializers.ValidationError(
                    {"details": {index: {"offer_type": "This field is required."}}}
                )

            detail = existing_details.get(offer_type)

            if detail is None:
                raise serializers.ValidationError(
                    {"details": {index: {"offer_type": "Invalid offer_type."}}}
                )

            features = detail_data.pop("features", None)

            for field, value in detail_data.items():
                setattr(detail, field, value)

            detail.save()

            if features is not None:
                detail.features.all().delete()
                OfferDetailFeature.objects.bulk_create(
                    [
                        OfferDetailFeature(
                            offer_detail=detail,
                            description=feature,
                        )
                        for feature in features
                    ]
                )

    def to_representation(self, instance):  # type:ignore
        """Return the updated offer using the retrieve response format."""
        return OfferRetrieveSerializer(
            instance,
            context=self.context,
        ).data

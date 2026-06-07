from rest_framework import serializers

from reviews_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Serialize review data."""

    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        """Define review serializer fields."""

        model = Review
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "reviewer",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        """Validate review creation rules."""
        request = self.context["request"]

        if request.method == "POST":
            business_user = attrs["business_user"]

            if business_user.type != "business":
                raise serializers.ValidationError(
                    {"business_user": "Selected user must be a business user."}
                )

            if Review.objects.filter(
                reviewer=request.user,
                business_user=business_user,
            ).exists():
                raise serializers.ValidationError(
                    {"detail": "You have already reviewed this business user."}
                )

        return attrs

    def update(self, instance, validated_data):
        """Update only editable review fields."""
        instance.rating = validated_data.get("rating", instance.rating)
        instance.description = validated_data.get("description", instance.description)
        instance.save(update_fields=["rating", "description", "updated_at"])
        return instance

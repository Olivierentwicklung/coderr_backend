from rest_framework import serializers

from reviews_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Serialize review data for list and create endpoints."""

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
        read_only_fields = ["id", "reviewer", "created_at", "updated_at"]

    def validate(self, attrs):
        """Validate that a customer can review a business user only once."""
        request = self.context["request"]
        user = request.user
        business_user = attrs.get("business_user")

        if business_user.type != "business":
            raise serializers.ValidationError(
                {"business_user": "Selected user must be a business user."}
            )

        if Review.objects.filter(reviewer=user, business_user=business_user).exists():
            raise serializers.ValidationError(
                {"detail": "You have already reviewed this business user."}
            )

        return attrs

    def create(self, validated_data):
        """Create a review with the authenticated user as reviewer."""
        request = self.context["request"]
        return Review.objects.create(reviewer=request.user, **validated_data)

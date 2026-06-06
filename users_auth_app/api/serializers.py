from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.

    Validates the registration data, ensures that both password fields
    match, and creates a new user with a hashed password.
    """

    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        """
        Configuration for the RegistrationSerializer.
        """

        model = User
        fields = [
            "username",
            "email",
            "password",
            "repeated_password",
            "type",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, attrs):
        """
        Validate that the password and repeated password match.

        Args:
            attrs (dict): Incoming validated serializer data.

        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If the passwords do not match.
        """
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        return attrs

    def create(self, validated_data):
        """
        Create and return a new user instance.

        Removes the repeated_password field from the validated data and
        creates the user using the custom user manager to ensure the
        password is properly hashed.

        Args:
            validated_data (dict): Validated registration data.

        Returns:
            User: The newly created user instance.
        """
        validated_data.pop("repeated_password")

        user = User.objects.create_user(  # type: ignore
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            type=validated_data["type"],
        )

        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """Validate credentials and attach the authenticated user."""
        user = authenticate(
            username=attrs.get("username"),
            password=attrs.get("password"),
        )

        if user is None:
            raise serializers.ValidationError(
                {"detail": "Invalid username or password."}
            )

        attrs["user"] = user
        return attrs


class ProfileDetailSerializer(serializers.ModelSerializer):
    """Serializer for retrieving and updating user profile data."""

    user = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        """Configure profile fields exposed by the API."""

        model = User
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
            "email",
            "created_at",
        ]
        read_only_fields = [
            "user",
            "username",
            "type",
            "created_at",
        ]


class ProfileListSerializer(serializers.ModelSerializer):
    """Serializer for listing public profile data."""

    user = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        """Configure fields returned in profile list endpoints."""

        model = User
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
        ]
        read_only_fields = fields

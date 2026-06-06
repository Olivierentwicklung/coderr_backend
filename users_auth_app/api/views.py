from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    LoginSerializer,
    ProfileDetailSerializer,
    RegistrationSerializer,
)

User = get_user_model()


class RegistrationView(APIView):
    """
    API endpoint for user registration.

    Allows unauthenticated users to create a new account.
    Upon successful registration, an authentication token
    is generated and returned together with basic user data.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Register a new user.

        Validates the incoming registration data, creates a new user,
        generates an authentication token, and returns the token along
        with the user's information.

        Args:
            request: The incoming HTTP request containing the registration data.

        Returns:
            Response:
                - 201 CREATED: User successfully registered.
                - 400 BAD REQUEST: Validation errors occurred.
                - 500 INTERNAL SERVER ERROR if an unexpected database error occurs.
        """
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "username": user.username,  # type: ignore
                "email": user.email,  # type: ignore
                "user_id": user.id,  # type: ignore
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """
    API endpoint for user login.

    Allows unauthenticated users to log in with username and password.
    Returns an authentication token and basic user data on success.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Log in a user and return an authentication token.

        Returns:
            Response:
                - 200 OK if login succeeds.
                - 400 BAD REQUEST if credentials are invalid.
                - 500 INTERNAL SERVER ERROR if an unexpected database error occurs.
        """

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]  # type:ignore
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id,
            },
            status=status.HTTP_200_OK,
        )


class ProfileDetailView(generics.RetrieveAPIView):
    """
    API endpoint for retrieving a user profile.

    Only authenticated users can access this endpoint.
    The profile is retrieved by the user's primary key from the URL.
    """

    queryset = User.objects.all()
    serializer_class = ProfileDetailSerializer
    permission_classes = [IsAuthenticated]

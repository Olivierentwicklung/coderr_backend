from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegistrationSerializer


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
        """
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
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

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

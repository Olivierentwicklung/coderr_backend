from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsProfileOwnerOrReadOnly
from .schema.base_schema import AUTH_TAG, PROFILE_TAG
from .schema.login_schema import LOGIN_DESCRIPTION, LOGIN_EXAMPLES
from .schema.profile_detail_retrieve_schema import (
    PROFILE_DETAIL_RETRIEVE_DESCRIPTION,
    PROFILE_DETAIL_RETRIEVE_EXAMPLES,
    PROFILE_DETAIL_RETRIEVE_PARAMETERS,
)
from .schema.profile_detail_update_schema import (
    PROFILE_DETAIL_UPDATE_DESCRIPTION,
    PROFILE_DETAIL_UPDATE_EXAMPLES,
    PROFILE_DETAIL_UPDATE_PARAMETERS,
)
from .schema.registration_schema import REGISTRATION_DESCRIPTION, REGISTRATION_EXAMPLES
from .serializers import (
    BusinessProfileListSerializer,
    CustomerProfileListSerializer,
    LoginSerializer,
    ProfileDetailSerializer,
    RegistrationSerializer,
)

User = get_user_model()


@extend_schema(
    tags=AUTH_TAG,
    description=REGISTRATION_DESCRIPTION,
    request=RegistrationSerializer,
    examples=REGISTRATION_EXAMPLES,
)
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


@extend_schema(
    tags=AUTH_TAG,
    description=LOGIN_DESCRIPTION,
    request=LoginSerializer,
    examples=LOGIN_EXAMPLES,
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


@extend_schema(tags=PROFILE_TAG)
@extend_schema_view(
    get=extend_schema(
        description=PROFILE_DETAIL_RETRIEVE_DESCRIPTION,
        parameters=PROFILE_DETAIL_RETRIEVE_PARAMETERS,
        responses={200: ProfileDetailSerializer},
        examples=PROFILE_DETAIL_RETRIEVE_EXAMPLES,
    ),
    put=extend_schema(
        description=PROFILE_DETAIL_UPDATE_DESCRIPTION,
        parameters=PROFILE_DETAIL_UPDATE_PARAMETERS,
        request=ProfileDetailSerializer,
        responses={200: ProfileDetailSerializer},
        examples=PROFILE_DETAIL_UPDATE_EXAMPLES,
    ),
    # patch=extend_schema(
    #     description=PROFILE_DETAIL_PARTIAL_UPDATE_DESCRIPTION,
    #     parameters=PROFILE_DETAIL_RETRIEVE_PARAMETERS,
    #     request=ProfileDetailSerializer,
    #     responses={200: ProfileDetailSerializer},
    #     examples=PROFILE_DETAIL_PARTIAL_UPDATE_EXAMPLES,
    # ),
)
class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for retrieving and updating user profiles.

    Authenticated users can retrieve profiles.
    Only the profile owner can update their own profile.
    """

    queryset = User.objects.all()
    serializer_class = ProfileDetailSerializer
    permission_classes = [IsAuthenticated, IsProfileOwnerOrReadOnly]


@extend_schema(tags=["Profile"])
class BusinessProfileListView(generics.ListAPIView):
    """
    API endpoint for listing business profiles.

    Only authenticated users can retrieve this list.
    The endpoint returns users whose type is business.
    """

    serializer_class = BusinessProfileListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):  # type:ignore
        """Return all business users with related profile file."""
        return User.objects.select_related("file").filter(type="business")


@extend_schema(tags=["Profile"])
class CustomerProfileListView(generics.ListAPIView):
    """
    API endpoint for listing customer profiles.

    Only authenticated users can retrieve this list.
    The endpoint returns users whose type is customer.
    """

    serializer_class = CustomerProfileListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):  # type:ignore
        """Return all users with the customer profile type."""
        return User.objects.select_related("file").filter(type="customer")

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory

from users_auth_app.api.views import RegistrationView

User = get_user_model()


@pytest.mark.django_db
def test_registration_performance_regression(
    registration_url,
    django_assert_num_queries,
    valid_registration_payload,
):
    factory = APIRequestFactory()
    request = factory.post(
        registration_url,
        valid_registration_payload,
        format="json",
    )

    view = RegistrationView.as_view()

    with django_assert_num_queries(7):
        response = view(request)

    assert response.status_code == 201


@pytest.mark.django_db
def test_registration_success_creates_user(
    api_client,
    registration_url,
    valid_registration_payload,
):
    """Test that a new user can register successfully."""
    response = api_client.post(
        registration_url,
        valid_registration_payload,
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(username="exampleUsername").exists()

    user = User.objects.get(username="exampleUsername")

    assert user.email == "example@mail.de"  # type:ignore
    assert user.type == "customer"  # type:ignore
    assert user.check_password("examplePassword")


@pytest.mark.django_db
def test_registration_success_returns_expected_response(
    api_client,
    registration_url,
    valid_registration_payload,
):
    """Test that registration returns token and user data."""
    response = api_client.post(
        registration_url,
        valid_registration_payload,
        format="json",
    )

    user = User.objects.get(username="exampleUsername")

    assert response.status_code == status.HTTP_201_CREATED
    assert "token" in response.data
    assert response.data["username"] == user.username  # type:ignore
    assert response.data["email"] == user.email  # type:ignore
    assert response.data["user_id"] == user.id  # type:ignore


@pytest.mark.django_db
def test_registration_success_creates_auth_token(
    api_client,
    registration_url,
    valid_registration_payload,
):
    """Test that an auth token is created for the registered user."""
    response = api_client.post(
        registration_url,
        valid_registration_payload,
        format="json",
    )

    user = User.objects.get(username="exampleUsername")
    token = Token.objects.get(user=user)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["token"] == token.key


@pytest.mark.django_db
def test_registration_requires_no_authentication(
    api_client,
    registration_url,
    valid_registration_payload,
):
    """Test that registration works without authentication."""
    response = api_client.post(
        registration_url,
        valid_registration_payload,
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
@pytest.mark.parametrize(
    "missing_field",
    [
        "username",
        "email",
        "password",
        "repeated_password",
        "type",
    ],
)
def test_registration_fails_when_required_field_is_missing(
    api_client,
    registration_url,
    valid_registration_payload,
    missing_field,
):
    """Test registration fails when a required field is missing."""
    payload = valid_registration_payload.copy()
    payload.pop(missing_field)

    response = api_client.post(
        registration_url,
        payload,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_registration_fails_when_passwords_do_not_match(
    api_client,
    registration_url,
    valid_registration_payload,
):
    """Test registration fails when passwords do not match."""
    payload = valid_registration_payload.copy()
    payload["repeated_password"] = "wrongPassword"

    response = api_client.post(
        registration_url,
        payload,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert User.objects.count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize(
    "invalid_type",
    [
        "admin",
        "staff",
        "",
        None,
    ],
)
def test_registration_fails_with_invalid_user_type(
    api_client,
    registration_url,
    valid_registration_payload,
    invalid_type,
):
    """Test registration fails when user type is invalid."""
    payload = valid_registration_payload.copy()
    payload["type"] = invalid_type

    response = api_client.post(
        registration_url,
        payload,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_registration_fails_with_duplicate_username(
    api_client,
    registration_url,
    valid_registration_payload,
):
    """Test registration fails when username already exists."""
    User.objects.create_user(  # type:ignore
        username="exampleUsername",
        email="other@mail.de",
        password="oldPassword",
        type="customer",
    )

    response = api_client.post(
        registration_url,
        valid_registration_payload,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_registration_fails_with_duplicate_email(
    api_client,
    registration_url,
    valid_registration_payload,
):
    """Test registration fails when email already exists."""
    User.objects.create_user(  # type:ignore
        username="otherUser",
        email="example@mail.de",
        password="oldPassword",
        type="customer",
    )

    response = api_client.post(
        registration_url,
        valid_registration_payload,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_registration_password_is_not_saved_as_plain_text(
    api_client,
    registration_url,
    valid_registration_payload,
):
    """Test that the password is hashed and not saved as plain text."""
    response = api_client.post(
        registration_url,
        valid_registration_payload,
        format="json",
    )

    user = User.objects.get(username="exampleUsername")

    assert response.status_code == status.HTTP_201_CREATED
    assert user.password != "examplePassword"
    assert user.check_password("examplePassword")


@pytest.mark.django_db
def test_registration_response_does_not_return_password(
    api_client,
    registration_url,
    valid_registration_payload,
):
    """Test that password fields are not returned in the response."""
    response = api_client.post(
        registration_url,
        valid_registration_payload,
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert "password" not in response.data
    assert "repeated_password" not in response.data


@pytest.mark.django_db
def test_registration_returns_500_when_unexpected_error_happens(
    api_client, registration_url, valid_registration_payload, force_db_crash
):

    with force_db_crash:
        response = api_client.post(
            registration_url,
            valid_registration_payload,
            format="json",
        )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

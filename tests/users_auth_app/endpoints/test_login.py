import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory

from users_auth_app.api.views import LoginView


@pytest.mark.django_db
def test_login_success_returns_token_and_user_data(
    api_client,
    login_url,
    valid_login_custom_user_payload,
    customer_user,
):
    response = api_client.post(
        login_url, valid_login_custom_user_payload, format="json"
    )

    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.data
    assert response.data["username"] == customer_user.username
    assert response.data["email"] == customer_user.email
    assert response.data["user_id"] == customer_user.id


@pytest.mark.django_db
def test_login_success_creates_token_if_not_exists(
    api_client,
    login_url,
    valid_login_business_user_payload,
    business_user,
):
    Token.objects.filter(user=business_user).delete()

    response = api_client.post(
        login_url, valid_login_business_user_payload, format="json"
    )

    token = Token.objects.get(user=business_user)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["token"] == token.key


@pytest.mark.django_db
def test_login_success_reuses_existing_token(
    api_client,
    login_url,
    valid_login_custom_user_payload,
    customer_user,
):
    existing_token = Token.objects.create(user=customer_user)

    response = api_client.post(
        login_url, valid_login_custom_user_payload, format="json"
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["token"] == existing_token.key
    assert Token.objects.filter(user=customer_user).count() == 1


@pytest.mark.django_db
def test_login_requires_no_authentication(
    api_client,
    login_url,
    valid_login_custom_user_payload,
):
    response = api_client.post(
        login_url, valid_login_custom_user_payload, format="json"
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.parametrize("missing_field", ["username", "password"])
def test_login_fails_when_required_field_is_missing(
    api_client,
    login_url,
    valid_login_custom_user_payload,
    missing_field,
):
    payload = valid_login_custom_user_payload.copy()
    payload.pop(missing_field)

    response = api_client.post(login_url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_login_fails_with_wrong_password(
    api_client,
    login_url,
    valid_login_custom_user_payload,
):
    payload = valid_login_custom_user_payload.copy()
    payload["password"] = "wrongPassword"

    response = api_client.post(login_url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_login_fails_with_unknown_username(
    api_client,
    login_url,
):
    payload = {
        "username": "unknownUser",
        "password": "testpassword123",
    }

    response = api_client.post(login_url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"username": ""},
        {"password": ""},
        {"username": "", "password": ""},
        {"username": None, "password": "testpassword123"},
        {"username": "customer", "password": None},
    ],
)
def test_login_fails_with_invalid_payload(
    api_client,
    login_url,
    payload,
):
    response = api_client.post(login_url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_login_response_does_not_return_password(
    api_client,
    login_url,
    valid_login_custom_user_payload,
):
    response = api_client.post(
        login_url, valid_login_custom_user_payload, format="json"
    )

    assert response.status_code == status.HTTP_200_OK
    assert "password" not in response.data


@pytest.mark.django_db
def test_login_returns_500_when_unexpected_error_happens(
    api_client,
    login_url,
    valid_login_custom_user_payload,
    force_db_crash,
):
    with force_db_crash:
        response = api_client.post(
            login_url, valid_login_custom_user_payload, format="json"
        )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.django_db
def test_login_query_count_performance(
    django_assert_num_queries,
    valid_login_custom_user_payload,
):
    factory = APIRequestFactory()
    request = factory.post(
        reverse("login"),
        valid_login_custom_user_payload,
        format="json",
    )

    view = LoginView.as_view()

    with django_assert_num_queries(5):
        response = view(request)

    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.data  # type:ignore

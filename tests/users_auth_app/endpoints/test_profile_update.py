import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from users_auth_app.api.views import ProfileDetailView


@pytest.mark.django_db
def test_profile_update_success_returns_updated_profile_data(
    authenticated_business,
    profile_update_url,
    valid_profile_update_payload,
    business_user,
):
    """Test profile owner can update own profile."""
    response = authenticated_business.patch(
        profile_update_url,
        valid_profile_update_payload,
        format="json",
    )

    business_user.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert response.data["user"] == business_user.id
    assert response.data["username"] == business_user.username
    assert response.data["first_name"] == valid_profile_update_payload["first_name"]
    assert response.data["last_name"] == valid_profile_update_payload["last_name"]
    assert response.data["location"] == valid_profile_update_payload["location"]
    assert response.data["tel"] == valid_profile_update_payload["tel"]
    assert response.data["description"] == valid_profile_update_payload["description"]
    assert (
        response.data["working_hours"] == valid_profile_update_payload["working_hours"]
    )
    assert response.data["email"] == valid_profile_update_payload["email"]
    assert response.data["type"] == business_user.type
    assert "file" in response.data
    assert "created_at" in response.data


@pytest.mark.django_db
def test_profile_update_saves_changes_to_database(
    authenticated_business,
    profile_update_url,
    valid_profile_update_payload,
    business_user,
):
    """Test profile update persists changes in database."""
    response = authenticated_business.patch(
        profile_update_url,
        valid_profile_update_payload,
        format="json",
    )

    business_user.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert business_user.first_name == "Max"
    assert business_user.last_name == "Mustermann"
    assert business_user.location == "Berlin"
    assert business_user.tel == "987654321"
    assert business_user.description == "Updated business description"
    assert business_user.working_hours == "10-18"
    assert business_user.email == "new_email@business.de"


@pytest.mark.django_db
def test_profile_update_allows_partial_update(
    authenticated_business,
    profile_update_url,
    business_user,
):
    """Test profile owner can update only selected fields."""
    payload = {"tel": "111222333"}

    response = authenticated_business.patch(
        profile_update_url,
        payload,
        format="json",
    )

    business_user.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert business_user.tel == "111222333"


@pytest.mark.django_db
def test_profile_update_requires_authentication(
    api_client,
    profile_update_url,
    valid_profile_update_payload,
):
    """Test unauthenticated users cannot update a profile."""
    response = api_client.patch(
        profile_update_url,
        valid_profile_update_payload,
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_profile_update_returns_403_when_user_is_not_owner(
    authenticated_customer,
    profile_update_url,
    valid_profile_update_payload,
    business_user,
):
    """Test authenticated users cannot update another user's profile."""
    response = authenticated_customer.patch(
        profile_update_url,
        valid_profile_update_payload,
        format="json",
    )

    business_user.refresh_from_db()

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert business_user.email != "new_email@business.de"


@pytest.mark.django_db
def test_profile_update_returns_404_when_profile_does_not_exist(
    authenticated_business,
    valid_profile_update_payload,
):
    """Test updating a non-existing profile returns 404."""
    url = reverse("profile-detail", kwargs={"pk": 999999})

    response = authenticated_business.patch(
        url,
        valid_profile_update_payload,
        format="json",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_profile_update_returns_500_when_unexpected_error_happens(
    authenticated_business,
    profile_update_url,
    valid_profile_update_payload,
    force_db_crash,
):

    with force_db_crash:
        response = authenticated_business.patch(
            profile_update_url,
            valid_profile_update_payload,
            format="json",
        )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.django_db
def test_profile_update_query_count_performance(
    django_assert_num_queries,
    profile_update_url,
    business_user,
    valid_profile_update_payload,
):
    """
    Performance regression test for profile update.

    Ensures updating a profile does not accidentally introduce
    additional database queries in the future.
    """
    factory = APIRequestFactory()
    request = factory.patch(
        profile_update_url,
        valid_profile_update_payload,
        format="json",
    )
    force_authenticate(request, user=business_user)

    view = ProfileDetailView.as_view()

    with django_assert_num_queries(3):
        response = view(request, pk=business_user.id)

    assert response.status_code == status.HTTP_200_OK

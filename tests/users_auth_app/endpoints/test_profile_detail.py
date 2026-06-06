import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from users_auth_app.api.views import ProfileDetailView


@pytest.mark.django_db
def test_profile_detail_success_returns_profile_data(
    authenticated_business,
    profile_detail_url,
    business_user,
):
    """Test authenticated users can retrieve a user profile."""
    response = authenticated_business.get(profile_detail_url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["user"] == business_user.id
    assert response.data["username"] == business_user.username
    assert response.data["first_name"] == business_user.first_name
    assert response.data["last_name"] == business_user.last_name
    assert response.data["type"] == business_user.type
    assert response.data["email"] == business_user.email
    assert "file" in response.data
    assert "location" in response.data
    assert "tel" in response.data
    assert "description" in response.data
    assert "working_hours" in response.data
    assert "created_at" in response.data


@pytest.mark.django_db
def test_profile_detail_requires_authentication(
    api_client,
    profile_detail_url,
):
    """Test unauthenticated users cannot retrieve a profile."""
    response = api_client.get(profile_detail_url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_profile_detail_returns_404_when_profile_does_not_exist(
    authenticated_customer,
):
    """Test retrieving a non-existing profile returns 404."""
    url = reverse("profile-detail", kwargs={"pk": 999999})

    response = authenticated_customer.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_profile_detail_returns_500_when_unexpected_error_happens(
    authenticated_business,
    profile_detail_url,
    force_db_crash,
):

    with force_db_crash:
        response = authenticated_business.get(profile_detail_url)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.django_db
def test_profile_detail_query_count_performance(
    django_assert_num_queries,
    profile_detail_url,
    business_user,
):
    """
    Performance regression test for profile detail.

    Ensures retrieving a profile does not accidentally introduce
    additional database queries in the future.
    """
    factory = APIRequestFactory()
    request = factory.get(profile_detail_url, kwargs={"pk": business_user.id})
    request.user = business_user

    force_authenticate(request, user=business_user)
    view = ProfileDetailView.as_view()

    with django_assert_num_queries(1):
        response = view(request, pk=business_user.id)

    assert response.status_code == status.HTTP_200_OK

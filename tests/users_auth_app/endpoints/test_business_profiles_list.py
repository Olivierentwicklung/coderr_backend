# tests/users_auth_app/endpoints/test_business_profiles_list.py

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from users_auth_app.api.views import BusinessProfileListView

User = get_user_model()


@pytest.mark.django_db
def test_business_profiles_list_success_returns_business_profiles(
    authenticated_customer,
    business_profiles_url,
    business_user,
    second_business_user,
):
    """Test authenticated users can retrieve all business profiles."""
    response = authenticated_customer.get(business_profiles_url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

    usernames = [profile["username"] for profile in response.data]

    assert business_user.username in usernames
    assert second_business_user.username in usernames

    for profile in response.data:
        assert profile["type"] == "business"
        assert "user" in profile
        assert "username" in profile
        assert "first_name" in profile
        assert "last_name" in profile
        assert "file" in profile
        assert "location" in profile
        assert "tel" in profile
        assert "description" in profile
        assert "working_hours" in profile
        assert "email" not in profile
        assert "created_at" not in profile


@pytest.mark.django_db
def test_business_profiles_list_does_not_return_customer_profiles(
    authenticated_customer,
    business_profiles_url,
    business_user,
    customer_user,
):
    """Test business profile list excludes customer users."""
    response = authenticated_customer.get(business_profiles_url)

    assert response.status_code == status.HTTP_200_OK

    usernames = [profile["username"] for profile in response.data]

    assert business_user.username in usernames
    assert customer_user.username not in usernames


@pytest.mark.django_db
def test_business_profiles_list_returns_empty_list_when_no_business_users_exist(
    authenticated_customer,
    business_profiles_url,
    business_user,
):
    """Test endpoint returns an empty list if no business users exist."""
    business_user.delete()

    response = authenticated_customer.get(business_profiles_url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == []


@pytest.mark.django_db
def test_business_profiles_list_requires_authentication(
    api_client,
    business_profiles_url,
):
    """Test unauthenticated users cannot retrieve business profiles."""
    response = api_client.get(business_profiles_url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_business_profiles_list_returns_500_when_unexpected_error_happens(
    authenticated_customer,
    business_profiles_url,
    force_db_crash,
):

    with force_db_crash:
        response = authenticated_customer.get(business_profiles_url)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.django_db
def test_business_profiles_list_query_count_performance(
    django_assert_num_queries,
    business_profiles_url,
    customer_user,
    business_user,
    second_business_user,
):
    """
    Performance regression test for business profiles list.

    Ensures listing business profiles does not introduce extra queries.
    """
    factory = APIRequestFactory()
    request = factory.get(business_profiles_url)
    force_authenticate(request, user=customer_user)

    view = BusinessProfileListView.as_view()

    with django_assert_num_queries(1):
        response = view(request)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2  # type:ignore

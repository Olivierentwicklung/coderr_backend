import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from users_auth_app.api.views import CustomerProfileListView

User = get_user_model()


@pytest.mark.django_db
def test_customer_profiles_list_success_returns_customer_profiles(
    authenticated_business,
    customer_profiles_url,
    customer_user,
    second_customer_user,
):
    """Test authenticated users can retrieve all customer profiles."""
    response = authenticated_business.get(customer_profiles_url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

    usernames = [profile["username"] for profile in response.data]

    assert customer_user.username in usernames
    assert second_customer_user.username in usernames

    for profile in response.data:
        assert profile["type"] == "customer"
        assert "user" in profile
        assert "username" in profile
        assert "first_name" in profile
        assert "last_name" in profile
        assert "file" in profile
        assert "uploaded_at" in profile
        assert "location" not in profile
        assert "tel" not in profile
        assert "description" not in profile
        assert "working_hours" not in profile
        assert "email" not in profile
        assert "created_at" not in profile


@pytest.mark.django_db
def test_customer_profiles_list_does_not_return_business_profiles(
    authenticated_customer,
    customer_profiles_url,
    customer_user,
    business_user,
):
    """Test customer profile list excludes business users."""
    response = authenticated_customer.get(customer_profiles_url)

    assert response.status_code == status.HTTP_200_OK

    usernames = [profile["username"] for profile in response.data]

    assert customer_user.username in usernames
    assert business_user.username not in usernames


@pytest.mark.django_db
def test_customer_profiles_list_returns_empty_list_when_no_customers_exist(
    authenticated_business,
    customer_profiles_url,
    customer_user,
):
    """Test endpoint returns an empty list if no customer users exist."""
    customer_user.delete()

    response = authenticated_business.get(customer_profiles_url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == []


@pytest.mark.django_db
def test_customer_profiles_list_requires_authentication(
    api_client,
    customer_profiles_url,
):
    """Test unauthenticated users cannot retrieve customer profiles."""
    response = api_client.get(customer_profiles_url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_customer_profiles_list_returns_500_when_unexpected_error_happens(
    authenticated_business,
    customer_profiles_url,
    force_db_crash,
):

    with force_db_crash:
        response = authenticated_business.get(customer_profiles_url)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.django_db
def test_customer_profiles_list_query_count_performance(
    django_assert_num_queries,
    customer_profiles_url,
    business_user,
    customer_user,
    second_customer_user,
):
    """
    Performance regression test for customer profiles list.

    Ensures listing customer profiles does not introduce extra queries.
    """
    factory = APIRequestFactory()
    request = factory.get(customer_profiles_url)
    force_authenticate(request, user=business_user)

    view = CustomerProfileListView.as_view()

    with django_assert_num_queries(1):
        response = view(request)

    assert response.status_code == status.HTTP_200_OK

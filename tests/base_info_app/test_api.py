import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory

from base_info_app.views import BaseInfoView


@pytest.mark.django_db
def test_base_info_returns_platform_statistics(
    api_client,
    base_info_url,
    review,
    second_review,
    offer,
    second_offer,
    business_user,
    second_business_user,
):
    """Verify that base info returns aggregated platform statistics."""
    # Arrange
    expected_fields = {
        "review_count",
        "average_rating",
        "business_profile_count",
        "offer_count",
    }

    # Act
    response = api_client.get(base_info_url)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert set(response.data.keys()) == expected_fields
    assert response.data["review_count"] == 2
    assert response.data["average_rating"] == 4.5
    assert response.data["business_profile_count"] == 2
    assert response.data["offer_count"] == 2


@pytest.mark.django_db
def test_base_info_allows_unauthenticated_access(
    api_client,
    base_info_url,
    review,
    offer,
    business_user,
):
    """Verify that unauthenticated users can access base info."""
    # Act
    response = api_client.get(base_info_url)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.data["review_count"] == 1
    assert response.data["average_rating"] == 4.0
    assert response.data["business_profile_count"] == 1
    assert response.data["offer_count"] == 1


@pytest.mark.django_db
def test_base_info_returns_zero_values_when_database_is_empty(
    api_client,
    base_info_url,
):
    """Verify that base info returns zero values when no relevant records exist."""
    # Act
    response = api_client.get(base_info_url)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "review_count": 0,
        "average_rating": 0.0,
        "business_profile_count": 0,
        "offer_count": 0,
    }


@pytest.mark.django_db
def test_base_info_counts_only_business_users_as_business_profiles(
    api_client,
    base_info_url,
    customer_user,
    second_customer_user,
    business_user,
):
    """Verify that customer users are excluded from business profile count."""
    # Act
    response = api_client.get(base_info_url)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.data["business_profile_count"] == 1


@pytest.mark.django_db
def test_base_info_returns_500_when_unexpected_database_error_occurs(
    api_client,
    base_info_url,
    force_db_crash,
):
    """Verify that unexpected database errors return HTTP 500."""
    # Act
    with force_db_crash:
        response = api_client.get(base_info_url)

    # Assert
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.django_db
def test_base_info_query_count_is_stable(
    django_assert_num_queries,
    business_user,
    second_business_user,
    review,
    second_review,
    offer,
    second_offer,
):
    """Verify that base info uses a stable number of database queries."""
    # Arrange

    factory = APIRequestFactory()
    request = factory.get(reverse("base-info"))
    view = BaseInfoView.as_view()

    # Act / Assert
    with django_assert_num_queries(4):
        response = view(request)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["review_count"] == 2  # type:ignore
    assert response.data["average_rating"] == 4.5  # type:ignore
    assert response.data["business_profile_count"] == 2  # type:ignore
    assert response.data["offer_count"] == 2  # type:ignore

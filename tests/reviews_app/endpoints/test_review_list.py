import pytest
from django.urls import resolve, reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate


@pytest.mark.django_db
def test_authenticated_user_can_list_reviews(
    authenticated_customer,
    reviews_list_url,
    review,
    second_review,
):
    """Verify authenticated users can retrieve the reviews list."""
    # Arrange / Act
    response = authenticated_customer.get(reviews_list_url)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

    first_result = response.data[0]
    assert set(first_result.keys()) == {
        "id",
        "business_user",
        "reviewer",
        "rating",
        "description",
        "created_at",
        "updated_at",
    }


@pytest.mark.django_db
def test_reviews_list_contains_expected_review_values(
    authenticated_customer,
    reviews_list_url,
    review,
):
    """Verify the reviews list contains all important review field values."""
    # Arrange / Act
    response = authenticated_customer.get(reviews_list_url)

    # Assert
    assert response.status_code == status.HTTP_200_OK

    result = response.data[0]
    assert result["id"] == review.id
    assert result["business_user"] == review.business_user_id
    assert result["reviewer"] == review.reviewer_id
    assert result["rating"] == review.rating
    assert result["description"] == review.description
    assert result["created_at"] is not None
    assert result["updated_at"] is not None


@pytest.mark.django_db
def test_reviews_list_requires_authentication(api_client, reviews_list_url, review):
    """Verify unauthenticated users cannot retrieve reviews."""
    # Arrange / Act
    response = api_client.get(reviews_list_url)

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_reviews_can_be_filtered_by_business_user_id(
    authenticated_customer,
    reviews_list_url,
    review,
    second_review,
):
    """Verify reviews can be filtered by business user ID."""
    # Arrange / Act
    response = authenticated_customer.get(
        reviews_list_url,
        {"business_user_id": review.business_user_id},
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["id"] == review.id
    assert response.data[0]["business_user"] == review.business_user_id


@pytest.mark.django_db
def test_reviews_can_be_filtered_by_reviewer_id(
    authenticated_customer,
    reviews_list_url,
    review,
    second_review,
):
    """Verify reviews can be filtered by reviewer ID."""
    # Arrange / Act
    response = authenticated_customer.get(
        reviews_list_url,
        {"reviewer_id": review.reviewer_id},
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["id"] == review.id
    assert response.data[0]["reviewer"] == review.reviewer_id


@pytest.mark.django_db
def test_reviews_can_be_ordered_by_rating(
    authenticated_customer,
    reviews_list_url,
    review,
    second_review,
):
    """Verify reviews can be ordered by rating."""
    # Arrange / Act
    response = authenticated_customer.get(reviews_list_url, {"ordering": "rating"})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    ratings = [item["rating"] for item in response.data]
    assert ratings == sorted(ratings)


@pytest.mark.django_db
def test_reviews_can_be_ordered_by_updated_at(
    authenticated_customer,
    reviews_list_url,
    review,
    second_review,
):
    """Verify reviews can be ordered by updated timestamp."""
    # Arrange / Act
    response = authenticated_customer.get(reviews_list_url, {"ordering": "updated_at"})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    updated_values = [item["updated_at"] for item in response.data]
    assert updated_values == sorted(updated_values)


@pytest.mark.django_db
def test_reviews_list_returns_500_when_database_crashes(
    authenticated_customer,
    reviews_list_url,
    review,
    force_db_crash,
):
    """Verify unexpected database errors return a 500 response."""
    # Arrange / Act
    with force_db_crash:
        response = authenticated_customer.get(reviews_list_url)

    # Assert
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.django_db
@pytest.mark.performance_regression
def test_reviews_list_query_count(
    django_assert_num_queries,
    customer_user,
    review,
    second_review,
):
    """Verify the reviews list endpoint query count does not regress."""
    # Arrange
    factory = APIRequestFactory()
    url = reverse("review-list")
    request = factory.get(url)
    force_authenticate(request, user=customer_user)

    view = resolve(url).func

    # Act / Assert
    with django_assert_num_queries(1):
        response = view(request)

    assert response.status_code == status.HTTP_200_OK

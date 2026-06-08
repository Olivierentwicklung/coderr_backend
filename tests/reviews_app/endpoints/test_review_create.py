import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from reviews_app.api.views import ReviewListCreateView
from reviews_app.models import Review


@pytest.mark.django_db
def test_customer_can_create_review(
    authenticated_customer,
    reviews_list_url,
    valid_review_create_payload,
    customer_user,
    business_user,
):
    """Verify authenticated customer users can create a review."""
    # Arrange / Act
    response = authenticated_customer.post(
        reviews_list_url,
        valid_review_create_payload,
        format="json",
    )

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert Review.objects.count() == 1

    created_review = Review.objects.get()
    assert response.data["id"] == created_review.pk
    assert response.data["business_user"] == business_user.pk
    assert response.data["reviewer"] == customer_user.pk
    assert response.data["rating"] == valid_review_create_payload["rating"]
    assert response.data["description"] == valid_review_create_payload["description"]
    assert response.data["created_at"] is not None
    assert response.data["updated_at"] is not None


@pytest.mark.django_db
def test_review_create_response_contains_expected_fields(
    authenticated_customer,
    reviews_list_url,
    valid_review_create_payload,
):
    """Verify review creation response contains the expected field structure."""
    # Arrange / Act
    response = authenticated_customer.post(
        reviews_list_url,
        valid_review_create_payload,
        format="json",
    )

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert set(response.data.keys()) == {
        "id",
        "business_user",
        "reviewer",
        "rating",
        "description",
        "created_at",
        "updated_at",
    }


@pytest.mark.django_db
def test_review_create_sets_authenticated_user_as_reviewer(
    authenticated_customer,
    reviews_list_url,
    valid_review_create_payload,
    customer_user,
):
    """Verify the reviewer is always taken from the authenticated user."""
    # Arrange
    payload = {
        **valid_review_create_payload,
        "reviewer": 9999,
    }

    # Act
    response = authenticated_customer.post(reviews_list_url, payload, format="json")

    # Assert
    assert response.status_code == status.HTTP_201_CREATED

    created_review = Review.objects.get()
    assert created_review.reviewer == customer_user
    assert response.data["reviewer"] == customer_user.pk


@pytest.mark.django_db
def test_review_create_requires_authentication(
    api_client,
    reviews_list_url,
    valid_review_create_payload,
):
    """Verify unauthenticated users cannot create reviews."""
    # Arrange / Act
    response = api_client.post(
        reviews_list_url,
        valid_review_create_payload,
        format="json",
    )

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Review.objects.count() == 0


@pytest.mark.django_db
def test_business_user_cannot_create_review(
    authenticated_business,
    reviews_list_url,
    valid_review_create_payload,
):
    """Verify business users are forbidden from creating reviews."""
    # Arrange / Act
    response = authenticated_business.post(
        reviews_list_url,
        valid_review_create_payload,
        format="json",
    )

    # Assert
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Review.objects.count() == 0


@pytest.mark.django_db
def test_customer_cannot_review_same_business_user_twice(
    authenticated_customer,
    reviews_list_url,
    valid_review_create_payload,
    review,
):
    """Verify customers cannot create duplicate reviews for one business user."""
    # Arrange / Act
    response = authenticated_customer.post(
        reviews_list_url,
        valid_review_create_payload,
        format="json",
    )

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Review.objects.count() == 1


@pytest.mark.django_db
def test_review_create_requires_business_user(
    authenticated_customer,
    reviews_list_url,
    valid_review_create_payload,
):
    """Verify business_user is required when creating a review."""
    # Arrange
    payload = valid_review_create_payload.copy()
    payload.pop("business_user")

    # Act
    response = authenticated_customer.post(reviews_list_url, payload, format="json")

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "business_user" in response.data
    assert Review.objects.count() == 0


@pytest.mark.django_db
def test_review_create_requires_rating(
    authenticated_customer,
    reviews_list_url,
    valid_review_create_payload,
):
    """Verify rating is required when creating a review."""
    # Arrange
    payload = valid_review_create_payload.copy()
    payload.pop("rating")

    # Act
    response = authenticated_customer.post(reviews_list_url, payload, format="json")

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "rating" in response.data
    assert Review.objects.count() == 0


@pytest.mark.django_db
def test_review_create_rejects_unknown_business_user(
    authenticated_customer,
    reviews_list_url,
    valid_review_create_payload,
):
    """Verify creating a review for an unknown business user fails."""
    # Arrange
    payload = {
        **valid_review_create_payload,
        "business_user": 9999,
    }

    # Act
    response = authenticated_customer.post(reviews_list_url, payload, format="json")

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "business_user" in response.data
    assert Review.objects.count() == 0


@pytest.mark.django_db
def test_review_create_rejects_customer_as_business_user(
    authenticated_customer,
    reviews_list_url,
    valid_review_create_payload,
    second_customer_user,
):
    """Verify reviews can only be created for business users."""
    # Arrange
    payload = {
        **valid_review_create_payload,
        "business_user": second_customer_user.pk,
    }

    # Act
    response = authenticated_customer.post(reviews_list_url, payload, format="json")

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Review.objects.count() == 0


@pytest.mark.django_db
def test_review_create_returns_500_when_database_crashes(
    authenticated_customer,
    reviews_list_url,
    valid_review_create_payload,
    force_db_crash,
):
    """Verify unexpected database errors return a 500 response."""
    # Arrange / Act
    with force_db_crash:
        response = authenticated_customer.post(
            reviews_list_url,
            valid_review_create_payload,
            format="json",
        )

    # Assert
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.django_db
def test_review_create_query_count(
    django_assert_num_queries,
    customer_user,
    business_user,
):
    """Verify review creation query count does not regress."""
    # Arrange
    payload = {
        "business_user": business_user.pk,
        "rating": 5,
        "description": "Top Qualität und schnelle Lieferung!",
    }
    factory = APIRequestFactory()
    request = factory.post(reverse("review-list"), payload, format="json")
    force_authenticate(request, user=customer_user)
    view = ReviewListCreateView.as_view()

    # Act / Assert
    with django_assert_num_queries(3):
        response = view(request)

    assert response.status_code == status.HTTP_201_CREATED

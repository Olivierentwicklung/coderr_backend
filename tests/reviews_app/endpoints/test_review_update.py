import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from reviews_app.api.views import ReviewDetailView


@pytest.mark.django_db
def test_review_owner_can_patch_review(
    authenticated_customer,
    review_detail_url,
    valid_review_patch_payload,
    review,
):
    """Verify the review owner can update rating and description."""
    # Arrange / Act
    response = authenticated_customer.patch(
        review_detail_url,
        valid_review_patch_payload,
        format="json",
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK

    review.refresh_from_db()
    assert review.rating == valid_review_patch_payload["rating"]
    assert review.description == valid_review_patch_payload["description"]

    assert response.data["id"] == review.pk
    assert response.data["business_user"] == review.business_user_id
    assert response.data["reviewer"] == review.reviewer_id
    assert response.data["rating"] == valid_review_patch_payload["rating"]
    assert response.data["description"] == valid_review_patch_payload["description"]
    assert response.data["created_at"] is not None
    assert response.data["updated_at"] is not None


@pytest.mark.django_db
def test_review_patch_response_contains_expected_fields(
    authenticated_customer,
    review_detail_url,
    valid_review_patch_payload,
):
    """Verify patch response contains the expected review fields."""
    # Arrange / Act
    response = authenticated_customer.patch(
        review_detail_url,
        valid_review_patch_payload,
        format="json",
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
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
def test_review_patch_updates_only_rating(
    authenticated_customer,
    review_detail_url,
    review,
):
    """Verify the owner can update only the rating field."""
    # Arrange
    payload = {"rating": 5}

    # Act
    response = authenticated_customer.patch(review_detail_url, payload, format="json")

    # Assert
    assert response.status_code == status.HTTP_200_OK

    review.refresh_from_db()
    assert review.rating == 5
    assert review.description == "Sehr professioneller Service."


@pytest.mark.django_db
def test_review_patch_updates_only_description(
    authenticated_customer,
    review_detail_url,
    review,
):
    """Verify the owner can update only the description field."""
    # Arrange
    payload = {"description": "Noch besser als erwartet!"}

    # Act
    response = authenticated_customer.patch(review_detail_url, payload, format="json")

    # Assert
    assert response.status_code == status.HTTP_200_OK

    review.refresh_from_db()
    assert review.rating == 4
    assert review.description == "Noch besser als erwartet!"


@pytest.mark.django_db
def test_review_patch_does_not_update_read_only_fields(
    authenticated_customer,
    review_detail_url,
    review,
    second_business_user,
    second_customer_user,
):
    """Verify business_user and reviewer cannot be changed through patch."""
    # Arrange
    payload = {
        "business_user": second_business_user.pk,
        "reviewer": second_customer_user.pk,
        "rating": 5,
        "description": "Noch besser als erwartet!",
    }

    # Act
    response = authenticated_customer.patch(review_detail_url, payload, format="json")

    # Assert
    assert response.status_code == status.HTTP_200_OK

    review.refresh_from_db()
    assert review.business_user_id != second_business_user.pk
    assert review.reviewer_id != second_customer_user.pk
    assert review.rating == 5
    assert review.description == "Noch besser als erwartet!"


@pytest.mark.django_db
def test_review_patch_requires_authentication(
    api_client,
    review_detail_url,
    valid_review_patch_payload,
    review,
):
    """Verify unauthenticated users cannot update reviews."""
    # Arrange / Act
    response = api_client.patch(
        review_detail_url,
        valid_review_patch_payload,
        format="json",
    )

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    review.refresh_from_db()
    assert review.rating == 4
    assert review.description == "Sehr professioneller Service."


@pytest.mark.django_db
def test_review_patch_forbidden_for_non_owner(
    api_client,
    second_customer_user,
    review_detail_url,
    valid_review_patch_payload,
    review,
):
    """Verify users who did not create the review cannot update it."""
    # Arrange
    api_client.force_authenticate(user=second_customer_user)

    # Act
    response = api_client.patch(
        review_detail_url,
        valid_review_patch_payload,
        format="json",
    )

    # Assert
    assert response.status_code == status.HTTP_403_FORBIDDEN

    review.refresh_from_db()
    assert review.rating == 4
    assert review.description == "Sehr professioneller Service."


@pytest.mark.django_db
def test_review_patch_returns_404_for_unknown_review(
    authenticated_customer,
    valid_review_patch_payload,
):
    """Verify patching an unknown review returns 404."""
    # Arrange
    url = reverse("review-detail", kwargs={"pk": 9999})

    # Act
    response = authenticated_customer.patch(
        url,
        valid_review_patch_payload,
        format="json",
    )

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_review_patch_rejects_invalid_rating(
    authenticated_customer,
    review_detail_url,
    review,
):
    """Verify invalid rating data returns 400 and does not update the review."""
    # Arrange
    payload = {"rating": "invalid"}

    # Act
    response = authenticated_customer.patch(review_detail_url, payload, format="json")

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "rating" in response.data

    review.refresh_from_db()
    assert review.rating == 4


@pytest.mark.django_db
def test_review_patch_returns_500_when_database_crashes(
    authenticated_customer,
    review_detail_url,
    valid_review_patch_payload,
    force_db_crash,
):
    """Verify unexpected database errors return a 500 response."""
    # Arrange / Act
    with force_db_crash:
        response = authenticated_customer.patch(
            review_detail_url,
            valid_review_patch_payload,
            format="json",
        )

    # Assert
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.django_db
def test_review_patch_query_count(
    django_assert_num_queries,
    customer_user,
    review,
):
    """Verify review patch query count does not regress."""
    # Arrange
    payload = {
        "rating": 5,
        "description": "Noch besser als erwartet!",
    }
    factory = APIRequestFactory()
    request = factory.patch(
        reverse("review-detail", kwargs={"pk": review.pk}),
        payload,
        format="json",
    )
    force_authenticate(request, user=customer_user)
    view = ReviewDetailView.as_view()

    # Act / Assert
    with django_assert_num_queries(3):
        response = view(request, pk=review.pk)

    assert response.status_code == status.HTTP_200_OK

# tests/reviews_app/endpoints/test_review_delete.py

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from reviews_app.api.views import ReviewDetailView
from reviews_app.models import Review


@pytest.mark.django_db
def test_review_owner_can_delete_review(
    authenticated_customer, review_detail_url, review
):
    """Verify the review owner can delete their own review."""
    response = authenticated_customer.delete(review_detail_url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data is None
    assert not Review.objects.filter(pk=review.pk).exists()


@pytest.mark.django_db
def test_review_delete_requires_authentication(api_client, review_detail_url, review):
    """Verify unauthenticated users cannot delete reviews."""
    response = api_client.delete(review_detail_url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Review.objects.filter(pk=review.pk).exists()


@pytest.mark.django_db
def test_review_delete_forbidden_for_non_owner(
    api_client,
    second_customer_user,
    review_detail_url,
    review,
):
    """Verify users cannot delete reviews they did not create."""
    api_client.force_authenticate(user=second_customer_user)

    response = api_client.delete(review_detail_url)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Review.objects.filter(pk=review.pk).exists()


@pytest.mark.django_db
def test_review_delete_returns_404_for_unknown_review(authenticated_customer):
    """Verify deleting an unknown review returns 404."""
    url = reverse("review-detail", kwargs={"pk": 9999})

    response = authenticated_customer.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
@pytest.mark.performance_regression
def test_review_delete_query_count(django_assert_num_queries, customer_user, review):
    """Verify review delete query count does not regress."""
    factory = APIRequestFactory()
    request = factory.delete(reverse("review-detail", kwargs={"pk": review.pk}))
    force_authenticate(request, user=customer_user)
    view = ReviewDetailView.as_view()

    with django_assert_num_queries(3):
        response = view(request, pk=review.pk)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_review_delete_returns_500_when_database_crashes(
    authenticated_customer,
    review_detail_url,
    force_db_crash,
):
    """Verify unexpected database errors return a 500 response when deleting a review."""
    # Arrange / Act
    with force_db_crash:
        response = authenticated_customer.delete(review_detail_url)

    # Assert
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

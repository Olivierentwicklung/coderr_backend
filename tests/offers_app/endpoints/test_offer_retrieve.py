import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from offers_app.api.views import OfferRetrieveUpdateDestroyView


@pytest.mark.django_db
def test_retrieve_offer_returns_200(
    authenticated_business,
    offer_detail_url,
):
    """Authenticated users can retrieve a single offer."""
    response = authenticated_business.get(offer_detail_url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_retrieve_offer_requires_authentication_401(
    api_client,
    offer_detail_url,
):
    """Unauthenticated users cannot retrieve a single offer."""
    response = api_client.get(offer_detail_url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_retrieve_offer_response_structure(
    authenticated_business,
    offer_detail_url,
):
    """Retrieve response contains the expected offer fields."""
    response = authenticated_business.get(offer_detail_url)

    expected_fields = {
        "id",
        "title",
        "user",
        "image",
        "description",
        "created_at",
        "updated_at",
        "details",
    }

    assert response.status_code == status.HTTP_200_OK
    assert expected_fields.issubset(response.data.keys())


@pytest.mark.django_db
def test_retrieve_offer_returns_offer_data(
    authenticated_business,
    offer_detail_url,
    offer,
):
    """Retrieve response contains the requested offer data."""
    response = authenticated_business.get(offer_detail_url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == offer.id
    assert response.data["title"] == offer.title
    assert response.data["description"] == offer.description
    assert response.data["image"] is None


@pytest.mark.django_db
def test_retrieve_offer_contains_three_details(
    authenticated_business,
    offer_detail_url,
):
    """Retrieve response contains all related offer details."""
    response = authenticated_business.get(offer_detail_url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["details"]) == 3


@pytest.mark.django_db
def test_retrieve_offer_detail_structure(
    authenticated_business,
    offer_detail_url,
):
    """Each returned offer detail contains the expected fields."""
    response = authenticated_business.get(offer_detail_url)

    first_detail = response.data["details"][0]

    expected_fields = {
        "id",
        "title",
        "revisions",
        "delivery_time_in_days",
        "price",
        "features",
        "offer_type",
    }

    assert response.status_code == status.HTTP_200_OK
    assert expected_fields.issubset(first_detail.keys())


@pytest.mark.django_db
def test_retrieve_offer_contains_detail_features(
    authenticated_business,
    offer_detail_url,
):
    """Offer detail features are returned as a list of strings."""
    response = authenticated_business.get(offer_detail_url)

    first_detail = response.data["details"][0]

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(first_detail["features"], list)
    assert first_detail["features"]


@pytest.mark.django_db
def test_retrieve_offer_returns_404_for_unknown_offer(
    authenticated_business,
):
    """Unknown offer IDs return 404."""
    url = reverse("offer-detail", kwargs={"pk": 999999})

    response = authenticated_business.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
@pytest.mark.performance_regression
def test_retrieve_offer_query_count(
    django_assert_num_queries,
    business_user,
    offer,
):
    """Retrieve offer endpoint should avoid unnecessary queries."""
    factory = APIRequestFactory()
    request = factory.get(f"/api/offers/{offer.pk}/")
    force_authenticate(request, user=business_user)

    view = OfferRetrieveUpdateDestroyView.as_view()

    with django_assert_num_queries(6):
        response = view(request, pk=offer.pk)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_retrieve_offer_returns_500_on_unexpected_error(
    authenticated_business,
    offer_detail_url,
    force_db_crash,
):
    """Unexpected database errors return 500."""
    with force_db_crash:
        response = authenticated_business.get(
            offer_detail_url,
            format="json",
        )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

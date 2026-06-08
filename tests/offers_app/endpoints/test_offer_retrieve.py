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
    response = authenticated_business.get(offer_detail_url)

    expected_fields = {
        "id",
        "user",
        "title",
        "image",
        "description",
        "created_at",
        "updated_at",
        "details",
        "min_price",
        "min_delivery_time",
    }

    assert response.status_code == status.HTTP_200_OK
    assert set(response.data.keys()) == expected_fields


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
def test_retrieve_offer_details_contain_only_id_and_url(
    authenticated_business,
    offer_detail_url,
):
    response = authenticated_business.get(offer_detail_url)

    assert response.status_code == status.HTTP_200_OK

    for detail in response.data["details"]:
        assert set(detail.keys()) == {"id", "url"}


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

    with django_assert_num_queries(5):
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

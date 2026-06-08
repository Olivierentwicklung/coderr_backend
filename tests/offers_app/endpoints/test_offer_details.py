import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from offers_app.api.views import OfferDetailRetrieveView


@pytest.mark.django_db
def test_retrieve_offer_detail_returns_200(
    authenticated_business,
    offer_detail_retrieve_url,
):
    """Authenticated users can retrieve an offer detail."""
    response = authenticated_business.get(offer_detail_retrieve_url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_retrieve_offer_detail_requires_authentication(
    api_client,
    offer_detail_retrieve_url,
):
    """Unauthenticated users cannot retrieve an offer detail."""
    response = api_client.get(offer_detail_retrieve_url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_retrieve_offer_detail_response_structure(
    authenticated_business,
    offer_detail_retrieve_url,
):
    """Offer detail response contains the expected fields."""
    response = authenticated_business.get(offer_detail_retrieve_url)

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
    assert expected_fields.issubset(response.data.keys())


@pytest.mark.django_db
def test_retrieve_offer_detail_returns_expected_data(
    authenticated_business,
    offer_detail_retrieve_url,
    offer_detail,
):
    """Offer detail response contains the requested detail data."""
    response = authenticated_business.get(offer_detail_retrieve_url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == offer_detail.id
    assert response.data["title"] == offer_detail.title
    assert response.data["revisions"] == offer_detail.revisions
    assert response.data["delivery_time_in_days"] == offer_detail.delivery_time_in_days
    assert response.data["price"] == offer_detail.price
    assert response.data["offer_type"] == offer_detail.offer_type


@pytest.mark.django_db
def test_retrieve_offer_detail_returns_features_as_list(
    authenticated_business,
    offer_detail_retrieve_url,
):
    """Offer detail features are returned as a list of strings."""
    response = authenticated_business.get(offer_detail_retrieve_url)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data["features"], list)
    assert response.data["features"]


@pytest.mark.django_db
def test_retrieve_offer_detail_returns_expected_features(
    authenticated_business,
    offer_detail_retrieve_url,
    offer_detail,
):
    """Offer detail response contains related feature descriptions."""
    response = authenticated_business.get(offer_detail_retrieve_url)

    expected_features = list(
        offer_detail.features.order_by("id").values_list("description", flat=True)
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["features"] == expected_features


@pytest.mark.django_db
def test_retrieve_offer_detail_returns_404_for_unknown_detail(
    authenticated_business,
):
    """Unknown offer detail IDs return 404."""
    url = reverse("offerdetail-detail", kwargs={"pk": 999999})

    response = authenticated_business.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_retrieve_offer_detail_query_count(
    django_assert_num_queries,
    business_user,
    offer_detail,
):
    """Offer detail retrieve endpoint should avoid unnecessary queries."""
    factory = APIRequestFactory()
    request = factory.get(f"/api/offerdetails/{offer_detail.pk}/")
    force_authenticate(request, user=business_user)

    view = OfferDetailRetrieveView.as_view()

    with django_assert_num_queries(3):
        response = view(request, pk=offer_detail.pk)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_retrieve_offer_detail_returns_500_on_unexpected_error(
    authenticated_business,
    offer_detail_retrieve_url,
    force_db_crash,
):
    """Unexpected database errors return 500."""
    with force_db_crash:
        response = authenticated_business.get(
            offer_detail_retrieve_url,
            format="json",
        )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from offers_app.api.views import OfferRetrieveUpdateDestroyView
from offers_app.models import Offer


@pytest.mark.django_db
def test_delete_offer_returns_204(
    authenticated_business,
    offer_detail_url,
):
    """Owner can delete an offer."""
    response = authenticated_business.delete(offer_detail_url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_delete_offer_removes_offer_from_database(
    authenticated_business,
    offer_detail_url,
    offer,
):
    """Deleting an offer removes it from the database."""
    response = authenticated_business.delete(offer_detail_url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Offer.objects.filter(pk=offer.pk).exists()


@pytest.mark.django_db
def test_delete_offer_returns_empty_response_body(
    authenticated_business,
    offer_detail_url,
):
    """Successful delete returns no response content."""
    response = authenticated_business.delete(offer_detail_url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""


@pytest.mark.django_db
def test_delete_offer_requires_authentication(
    api_client,
    offer_detail_url,
):
    """Unauthenticated users cannot delete offers."""
    response = api_client.delete(offer_detail_url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_delete_offer_forbidden_for_non_owner(
    authenticated_customer,
    offer_detail_url,
):
    """Users who do not own the offer cannot delete it."""
    response = authenticated_customer.delete(offer_detail_url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_delete_offer_returns_404_for_unknown_offer(
    authenticated_business,
):
    """Deleting an unknown offer returns 404."""
    url = reverse("offer-detail", kwargs={"pk": 999999})

    response = authenticated_business.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_offer_query_count(
    django_assert_num_queries,
    business_user,
    offer,
):
    """Delete offer endpoint should avoid unnecessary queries."""
    factory = APIRequestFactory()
    request = factory.delete(f"/api/offers/{offer.pk}/")
    force_authenticate(request, user=business_user)

    view = OfferRetrieveUpdateDestroyView.as_view()

    with django_assert_num_queries(8):
        response = view(request, pk=offer.pk)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_delete_offer_returns_500_on_unexpected_error(
    authenticated_business,
    offer_detail_url,
    force_db_crash,
):
    """Unexpected database errors return 500."""
    with force_db_crash:
        response = authenticated_business.delete(
            offer_detail_url,
            format="json",
        )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

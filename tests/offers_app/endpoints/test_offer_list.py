import pytest
from rest_framework import status
from rest_framework.test import APIRequestFactory

from offers_app.api.views import OfferListCreateView


@pytest.mark.django_db
def test_list_offers_returns_200(api_client, offers_list_url, offer):
    response = api_client.get(offers_list_url)

    assert response.status_code == status.HTTP_200_OK
    assert "count" in response.data
    assert "results" in response.data


@pytest.mark.django_db
def test_list_offers_is_public(api_client, offers_list_url, offer):
    response = api_client.get(offers_list_url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_list_offers_response_structure(api_client, offers_list_url, offer):
    response = api_client.get(offers_list_url)

    result = response.data["results"][0]

    expected_keys = {
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
        "user_details",
    }

    assert expected_keys.issubset(result.keys())


@pytest.mark.django_db
def test_offer_contains_user_details(api_client, offers_list_url, offer):
    response = api_client.get(offers_list_url)

    result = next(item for item in response.data["results"] if item["id"] == offer.id)

    assert result["user_details"] == {
        "first_name": offer.business_user.first_name,
        "last_name": offer.business_user.last_name,
        "username": offer.business_user.username,
    }


@pytest.mark.django_db
def test_offer_contains_min_price(api_client, offers_list_url, offer):
    response = api_client.get(offers_list_url)

    assert response.data["results"][0]["min_price"] == 100


@pytest.mark.django_db
def test_offer_contains_min_delivery_time(api_client, offers_list_url, offer):
    response = api_client.get(offers_list_url)

    assert response.data["results"][0]["min_delivery_time"] == 5


@pytest.mark.django_db
def test_filter_by_creator_id(
    api_client,
    offers_list_url,
    offer,
    second_offer,
    business_user,
):
    response = api_client.get(offers_list_url, {"creator_id": business_user.id})

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0]["id"] == offer.id


@pytest.mark.django_db
def test_filter_by_min_price(api_client, offers_list_url, offer, second_offer):
    response = api_client.get(offers_list_url, {"min_price": 100})

    returned_ids = [item["id"] for item in response.data["results"]]

    assert offer.id in returned_ids
    assert second_offer.id not in returned_ids


@pytest.mark.django_db
def test_filter_by_max_delivery_time(api_client, offers_list_url, offer, second_offer):
    response = api_client.get(offers_list_url, {"max_delivery_time": 3})

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0]["id"] == second_offer.id


@pytest.mark.django_db
def test_search_by_title(api_client, offers_list_url, offer, second_offer):
    response = api_client.get(offers_list_url, {"search": "Website"})

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0]["id"] == offer.id


@pytest.mark.django_db
def test_search_by_description(api_client, offers_list_url, offer, second_offer):
    response = api_client.get(offers_list_url, {"search": "branding"})

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0]["id"] == second_offer.id


@pytest.mark.django_db
def test_ordering_by_min_price(api_client, offers_list_url, offer, second_offer):
    response = api_client.get(offers_list_url, {"ordering": "min_price"})

    prices = [item["min_price"] for item in response.data["results"]]

    assert prices == sorted(prices)


@pytest.mark.django_db
def test_ordering_by_updated_at(api_client, offers_list_url, offer, second_offer):
    response = api_client.get(offers_list_url, {"ordering": "updated_at"})

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_page_size(api_client, offers_list_url, offer, second_offer):
    response = api_client.get(offers_list_url, {"page_size": 1})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 1


@pytest.mark.django_db
def test_empty_offer_list(api_client, offers_list_url):
    response = api_client.get(offers_list_url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 0
    assert response.data["results"] == []


@pytest.mark.django_db
@pytest.mark.parametrize(
    "params",
    [
        {"creator_id": "abc"},
        {"min_price": "abc"},
        {"max_delivery_time": "abc"},
        {"page_size": "abc"},
    ],
)
def test_invalid_query_parameters_return_400(api_client, offers_list_url, params):
    response = api_client.get(offers_list_url, params)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_ordering_by_updated_at_descending(
    api_client, offers_list_url, offer, second_offer
):
    response = api_client.get(offers_list_url, {"ordering": "-updated_at"})

    assert response.status_code == status.HTTP_200_OK

    updated_values = [item["updated_at"] for item in response.data["results"]]

    assert updated_values == sorted(updated_values, reverse=True)


@pytest.mark.django_db
def test_ordering_by_min_price_descending(
    api_client, offers_list_url, offer, second_offer
):
    response = api_client.get(offers_list_url, {"ordering": "-min_price"})

    assert response.status_code == status.HTTP_200_OK

    prices = [item["min_price"] for item in response.data["results"]]

    assert prices == sorted(prices, reverse=True)


@pytest.mark.django_db
def test_invalid_ordering_parameter_returns_400(api_client, offers_list_url):
    response = api_client.get(
        offers_list_url,
        {"ordering": "invalid_field"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_offer_list_query_count(
    django_assert_num_queries,
    offers_list_url,
    offer,
    second_offer,
):
    factory = APIRequestFactory()
    request = factory.get(offers_list_url)

    view = OfferListCreateView.as_view()

    with django_assert_num_queries(3):
        response = view(request)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_offer_list_returns_500_on_unexpected_error(
    api_client, offers_list_url, offer, force_db_crash
):

    with force_db_crash:
        response = api_client.get(
            offers_list_url,
            format="json",
        )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

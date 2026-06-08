import pytest
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from offers_app.api.views import OfferCreateSerializer, OfferListCreateView
from offers_app.models import Offer, OfferDetail


@pytest.mark.django_db
def test_offer_create_serializer_rejects_not_exactly_three_details():
    serializer = OfferCreateSerializer(
        data={
            "title": "Test offer",
            "description": "Test description",
            "details": [],
        }
    )

    assert not serializer.is_valid()
    assert "details" in serializer.errors


@pytest.mark.django_db
def test_create_offer_returns_201(
    authenticated_business,
    offers_list_url,
    offer_create_payload,
):

    response = authenticated_business.post(
        offers_list_url,
        offer_create_payload,
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == offer_create_payload["title"]
    assert response.data["description"] == offer_create_payload["description"]
    assert response.data["image"] is None
    assert len(response.data["details"]) == 3


@pytest.mark.django_db
def test_create_offer_creates_offer_in_database(
    authenticated_business,
    offers_list_url,
    business_user,
    offer_create_payload,
):

    response = authenticated_business.post(
        offers_list_url,
        offer_create_payload,
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert Offer.objects.count() == 1

    offer = Offer.objects.first()

    assert offer.title == offer_create_payload["title"]  # type:ignore
    assert offer.description == offer_create_payload["description"]  # type:ignore
    assert offer.business_user == business_user  # type:ignore


@pytest.mark.django_db
def test_create_offer_creates_three_details(
    authenticated_business,
    offers_list_url,
    business_user,
    offer_create_payload,
):

    response = authenticated_business.post(
        offers_list_url,
        offer_create_payload,
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert OfferDetail.objects.count() == 3

    detail_titles = list(
        OfferDetail.objects.order_by("id").values_list("title", flat=True)
    )

    assert detail_titles == [
        "Basic Design",
        "Standard Design",
        "Premium Design",
    ]


@pytest.mark.django_db
def test_create_offer_response_contains_detail_data(
    authenticated_business,
    offers_list_url,
    business_user,
    offer_create_payload,
):

    response = authenticated_business.post(
        offers_list_url,
        offer_create_payload,
        format="json",
    )

    first_detail = response.data["details"][0]

    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in first_detail
    assert first_detail["title"] == "Basic Design"
    assert first_detail["revisions"] == 2
    assert first_detail["delivery_time_in_days"] == 5
    assert first_detail["price"] in [100, "100.00", "100"]
    assert first_detail["features"] == ["Logo Design", "Visitenkarte"]
    assert first_detail["offer_type"] == "basic"


@pytest.mark.django_db
def test_create_offer_requires_authentication(
    api_client,
    offers_list_url,
    offer_create_payload,
):
    response = api_client.post(
        offers_list_url,
        offer_create_payload,
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create_offer_forbidden_for_customer_user(
    authenticated_customer,
    offers_list_url,
    customer_user,
    offer_create_payload,
):

    response = authenticated_customer.post(
        offers_list_url,
        offer_create_payload,
        format="json",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_create_offer_requires_exactly_three_details(
    authenticated_business,
    offers_list_url,
    business_user,
    offer_create_payload,
):

    offer_create_payload["details"] = offer_create_payload["details"][:2]

    response = authenticated_business.post(
        offers_list_url,
        offer_create_payload,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Offer.objects.count() == 0
    assert OfferDetail.objects.count() == 0


@pytest.mark.django_db
def test_create_offer_rejects_more_than_three_details(
    authenticated_business,
    offers_list_url,
    business_user,
    offer_create_payload,
):

    offer_create_payload["details"].append(
        {
            "title": "Extra Design",
            "revisions": 12,
            "delivery_time_in_days": 14,
            "price": 800,
            "features": ["Extra Feature"],
            "offer_type": "extra",
        }
    )

    response = authenticated_business.post(
        offers_list_url,
        offer_create_payload,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Offer.objects.count() == 0
    assert OfferDetail.objects.count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize(
    "field",
    ["title", "description", "details"],
)
def test_create_offer_requires_main_fields(
    authenticated_business,
    offers_list_url,
    business_user,
    offer_create_payload,
    field,
):

    offer_create_payload.pop(field)

    response = authenticated_business.post(
        offers_list_url,
        offer_create_payload,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@pytest.mark.parametrize(
    "field",
    [
        "title",
        "revisions",
        "delivery_time_in_days",
        "price",
        "features",
        "offer_type",
    ],
)
def test_create_offer_requires_detail_fields(
    authenticated_business,
    offers_list_url,
    business_user,
    offer_create_payload,
    field,
):

    offer_create_payload["details"][0].pop(field)

    response = authenticated_business.post(
        offers_list_url,
        offer_create_payload,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_offer_rejects_empty_features(
    authenticated_business,
    offers_list_url,
    business_user,
    offer_create_payload,
):

    offer_create_payload["details"][0]["features"] = []

    response = authenticated_business.post(
        offers_list_url,
        offer_create_payload,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@pytest.mark.performance_regression
def test_create_offer_query_count(
    django_assert_num_queries,
    offers_list_url,
    business_user,
    offer_create_payload,
):
    factory = APIRequestFactory()
    request = factory.post(
        offers_list_url,
        offer_create_payload,
        format="json",
    )
    # request.user = business_user
    force_authenticate(request, user=business_user)

    view = OfferListCreateView.as_view()

    with django_assert_num_queries(13):
        response = view(request)

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_offer_returns_500_on_unexpected_error(
    authenticated_business,
    offers_list_url,
    business_user,
    offer_create_payload,
    force_db_crash,
):

    with force_db_crash:
        response = authenticated_business.post(
            offers_list_url,
            offer_create_payload,
            format="json",
        )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

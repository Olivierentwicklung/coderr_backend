import pytest
from django.urls import reverse
from rest_framework import serializers, status
from rest_framework.test import APIRequestFactory, force_authenticate

from offers_app.api.serializers import OfferUpdateSerializer
from offers_app.api.views import OfferRetrieveUpdateDestroyView
from offers_app.models import OfferDetail


@pytest.mark.django_db
def test_offer_update_without_details_updates_only_offer(offer):
    serializer = OfferUpdateSerializer(
        offer,
        data={"title": "Updated title"},
        partial=True,
    )

    assert serializer.is_valid(), serializer.errors

    updated_offer = serializer.save()
    updated_offer.refresh_from_db()  # type:ignore

    assert updated_offer.title == "Updated title"  # type:ignore


@pytest.mark.django_db
def test_offer_update_detail_without_features(offer):
    detail = offer.details.first()

    serializer = OfferUpdateSerializer(
        offer,
        data={
            "details": [
                {
                    "offer_type": detail.offer_type,
                    "price": 999,
                }
            ]
        },
        partial=True,
    )

    assert serializer.is_valid(), serializer.errors

    serializer.save()
    detail.refresh_from_db()

    assert detail.price == 999


@pytest.mark.django_db
def test_offer_update_detail_with_features(offer):
    detail = offer.details.first()

    serializer = OfferUpdateSerializer(
        offer,
        data={
            "details": [
                {
                    "offer_type": detail.offer_type,
                    "features": ["New feature 1", "New feature 2"],
                }
            ]
        },
        partial=True,
    )

    assert serializer.is_valid(), serializer.errors

    serializer.save()
    detail.refresh_from_db()

    assert list(detail.features.values_list("description", flat=True)) == [
        "New feature 1",
        "New feature 2",
    ]


@pytest.mark.django_db
def test_offer_update_rejects_missing_offer_type_in_details(offer):
    serializer = OfferUpdateSerializer(
        offer,
        data={
            "details": [
                {
                    "price": 999,
                }
            ]
        },
        partial=True,
    )

    assert not serializer.is_valid()
    assert "details" in serializer.errors


@pytest.mark.django_db
def test_offer_update_rejects_duplicate_offer_type(offer):
    detail = offer.details.first()

    serializer = OfferUpdateSerializer(
        offer,
        data={
            "details": [
                {"offer_type": detail.offer_type, "price": 100},
                {"offer_type": detail.offer_type, "price": 200},
            ]
        },
        partial=True,
    )

    assert not serializer.is_valid()
    assert "details" in serializer.errors


@pytest.mark.django_db
def test_offer_update_rejects_valid_but_unknown_offer_type_inside_update(
    offer,
):
    first_detail = offer.details.first()

    # Remove all details except one, so another valid offer_type becomes "unknown"
    offer.details.exclude(pk=first_detail.pk).delete()

    existing_offer_types = set(offer.details.values_list("offer_type", flat=True))

    unused_offer_type = next(
        choice_value
        for choice_value, _ in OfferDetail.OFFER_TYPE_CHOICES
        if choice_value not in existing_offer_types
    )

    serializer = OfferUpdateSerializer(
        offer,
        data={
            "details": [
                {
                    "offer_type": unused_offer_type,
                    "price": 999,
                }
            ]
        },
        partial=True,
    )

    assert serializer.is_valid(), serializer.errors

    with pytest.raises(serializers.ValidationError):
        serializer.save()


@pytest.mark.django_db
def test_update_offer_returns_200(
    authenticated_business,
    offer_detail_url,
    offer_patch_payload,
):
    """Owner can update an offer."""
    response = authenticated_business.patch(
        offer_detail_url,
        offer_patch_payload,
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_update_offer_updates_title(
    authenticated_business,
    offer_detail_url,
    offer,
    offer_patch_payload,
):
    """PATCH updates only the submitted title."""
    response = authenticated_business.patch(
        offer_detail_url,
        offer_patch_payload,
        format="json",
    )

    offer.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert offer.title == "Updated Grafikdesign-Paket"
    assert response.data["title"] == "Updated Grafikdesign-Paket"


@pytest.mark.django_db
def test_update_offer_keeps_unsubmitted_fields(
    authenticated_business,
    offer_detail_url,
    offer,
    offer_patch_payload,
):
    """PATCH keeps fields that were not submitted."""
    old_description = offer.description

    response = authenticated_business.patch(
        offer_detail_url,
        offer_patch_payload,
        format="json",
    )

    offer.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert offer.description == old_description
    assert response.data["description"] == old_description


@pytest.mark.django_db
def test_update_offer_updates_basic_detail_by_offer_type(
    authenticated_business,
    offer_detail_url,
    offer,
    offer_patch_payload,
):
    """PATCH updates a detail using its offer_type."""
    basic_detail = offer.details.get(offer_type="basic")
    old_detail_id = basic_detail.id

    response = authenticated_business.patch(
        offer_detail_url,
        offer_patch_payload,
        format="json",
    )

    basic_detail.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert basic_detail.id == old_detail_id
    assert basic_detail.title == "Basic Design Updated"
    assert basic_detail.revisions == 3
    assert basic_detail.delivery_time_in_days == 6
    assert basic_detail.price == 120


@pytest.mark.django_db
def test_update_offer_updates_basic_detail_features(
    authenticated_business,
    offer_detail_url,
    offer,
    offer_patch_payload,
):
    """PATCH replaces features for the updated detail."""
    response = authenticated_business.patch(
        offer_detail_url,
        offer_patch_payload,
        format="json",
    )

    basic_detail = offer.details.get(offer_type="basic")
    features = list(
        basic_detail.features.order_by("id").values_list("description", flat=True)
    )

    assert response.status_code == status.HTTP_200_OK
    assert features == ["Logo Design", "Flyer"]


@pytest.mark.django_db
def test_update_offer_keeps_other_details_unchanged(
    authenticated_business,
    offer_detail_url,
    offer,
    offer_patch_payload,
):
    """PATCH does not overwrite details that were not submitted."""
    standard_detail = offer.details.get(offer_type="standard")
    old_title = standard_detail.title
    old_price = standard_detail.price

    response = authenticated_business.patch(
        offer_detail_url,
        offer_patch_payload,
        format="json",
    )

    standard_detail.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert standard_detail.title == old_title
    assert standard_detail.price == old_price


@pytest.mark.django_db
def test_update_offer_response_contains_all_details(
    authenticated_business,
    offer_detail_url,
    offer_patch_payload,
):
    """PATCH response returns all offer details."""
    response = authenticated_business.patch(
        offer_detail_url,
        offer_patch_payload,
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["details"]) == 3


@pytest.mark.django_db
def test_update_offer_response_detail_ids_are_preserved(
    authenticated_business,
    offer_detail_url,
    offer,
    offer_patch_payload,
):
    """PATCH keeps existing offer detail IDs."""
    old_ids = set(offer.details.values_list("id", flat=True))

    response = authenticated_business.patch(
        offer_detail_url,
        offer_patch_payload,
        format="json",
    )

    response_ids = {detail["id"] for detail in response.data["details"]}

    assert response.status_code == status.HTTP_200_OK
    assert response_ids == old_ids


@pytest.mark.django_db
def test_update_offer_requires_authentication(
    api_client,
    offer_detail_url,
    offer_patch_payload,
):
    """Unauthenticated users cannot update offers."""
    response = api_client.patch(
        offer_detail_url,
        offer_patch_payload,
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_offer_forbidden_for_non_owner(
    authenticated_customer,
    offer_detail_url,
    offer_patch_payload,
):
    """Users who do not own the offer cannot update it."""
    response = authenticated_customer.patch(
        offer_detail_url,
        offer_patch_payload,
        format="json",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_update_offer_returns_404_for_unknown_offer(
    authenticated_business,
    offer_patch_payload,
):
    """Unknown offer IDs return 404."""
    url = reverse("offer-detail", kwargs={"pk": 999999})

    response = authenticated_business.patch(
        url,
        offer_patch_payload,
        format="json",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_offer_returns_400_without_offer_type(
    authenticated_business,
    offer_detail_url,
    offer_patch_payload,
):
    """Detail updates require offer_type to identify the detail."""
    offer_patch_payload["details"][0].pop("offer_type")

    response = authenticated_business.patch(
        offer_detail_url,
        offer_patch_payload,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_update_offer_returns_400_for_unknown_offer_type(
    authenticated_business,
    offer_detail_url,
    offer_patch_payload,
):
    """Unknown detail offer_type returns 400."""
    offer_patch_payload["details"][0]["offer_type"] = "invalid"

    response = authenticated_business.patch(
        offer_detail_url,
        offer_patch_payload,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_update_offer_returns_400_for_empty_features(
    authenticated_business,
    offer_detail_url,
    offer_patch_payload,
):
    """Updated detail features cannot be empty."""
    offer_patch_payload["details"][0]["features"] = []

    response = authenticated_business.patch(
        offer_detail_url,
        offer_patch_payload,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_update_offer_returns_400_when_valid_offer_type_is_not_on_offer(
    authenticated_business,
    offer_detail_url,
    offer_patch_payload,
    offer,
):
    """PATCH returns 400 when a valid offer_type is not present on this offer."""
    offer.details.filter(offer_type="premium").delete()

    offer_patch_payload["details"][0]["offer_type"] = "premium"

    response = authenticated_business.patch(
        offer_detail_url,
        offer_patch_payload,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "details" in response.data


@pytest.mark.django_db
def test_update_offer_returns_400_for_duplicate_offer_types(
    authenticated_business,
    offer_detail_url,
):
    """Each offer_type may only be submitted once."""
    payload = {
        "details": [
            {
                "offer_type": "basic",
                "title": "Basic Design Updated",
            },
            {
                "offer_type": "basic",
                "title": "Another Basic Update",
            },
        ]
    }

    response = authenticated_business.patch(
        offer_detail_url,
        payload,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "details" in response.data


@pytest.mark.django_db
def test_update_details_raises_error_when_offer_type_missing(offer):
    """_update_details raises ValidationError when offer_type is missing."""
    serializer = OfferUpdateSerializer()

    details_data = [
        {
            "title": "Basic Design Updated",
            "revisions": 3,
            "delivery_time_in_days": 6,
            "price": 120,
            "features": ["Logo Design", "Flyer"],
        }
    ]

    with pytest.raises(serializers.ValidationError) as exc_info:
        serializer._update_details(offer, details_data)  # type:ignore

    assert exc_info.value.detail == {
        "details": {0: {"offer_type": "This field is required."}}
    }


@pytest.mark.django_db
def test_update_offer_query_count(
    django_assert_num_queries,
    business_user,
    offer,
    offer_patch_payload,
):
    """PATCH offer endpoint should avoid unnecessary queries."""
    factory = APIRequestFactory()
    request = factory.patch(
        f"/api/offers/{offer.pk}/",
        offer_patch_payload,
        format="json",
    )
    force_authenticate(request, user=business_user)

    view = OfferRetrieveUpdateDestroyView.as_view()

    with django_assert_num_queries(14):
        response = view(request, pk=offer.pk)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_update_offer_returns_500_on_unexpected_error(
    authenticated_business,
    offer_detail_url,
    offer_patch_payload,
    force_db_crash,
):
    """Unexpected database errors return 500."""
    with force_db_crash:
        response = authenticated_business.patch(
            offer_detail_url,
            offer_patch_payload,
            format="json",
        )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

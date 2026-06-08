import pytest
from rest_framework import status

from orders_app.models import Order


@pytest.mark.django_db
def test_create_order_as_customer_success(
    authenticated_customer,
    orders_list_url,
    customer_user,
    offer_detail,
):
    """Create an order from an offer detail as an authenticated customer."""
    payload = {"offer_detail_id": offer_detail.id}

    response = authenticated_customer.post(orders_list_url, payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Order.objects.count() == 1

    order = Order.objects.first()

    assert response.data["id"] == order.id  # type:ignore
    assert response.data["customer_user"] == customer_user.id
    assert response.data["business_user"] == offer_detail.offer.business_user.id
    assert response.data["title"] == offer_detail.title
    assert response.data["revisions"] == offer_detail.revisions
    assert response.data["delivery_time_in_days"] == offer_detail.delivery_time_in_days
    assert response.data["price"] == offer_detail.price
    assert response.data["offer_type"] == offer_detail.offer_type
    assert response.data["status"] == "in_progress"
    assert response.data["features"] == [
        feature.description for feature in offer_detail.features.all()
    ]


@pytest.mark.django_db
def test_create_order_requires_authentication(
    api_client, orders_list_url, offer_detail
):
    """Reject unauthenticated users when creating an order."""
    payload = {"offer_detail_id": offer_detail.id}

    response = api_client.post(orders_list_url, payload, format="json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Order.objects.count() == 0


@pytest.mark.django_db
def test_create_order_requires_customer_user(
    authenticated_business,
    orders_list_url,
    offer_detail,
):
    """Reject business users when creating an order."""
    payload = {"offer_detail_id": offer_detail.id}

    response = authenticated_business.post(orders_list_url, payload, format="json")

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Order.objects.count() == 0


@pytest.mark.django_db
def test_create_order_requires_offer_detail_id(authenticated_customer, orders_list_url):
    """Reject order creation when offer_detail_id is missing."""
    response = authenticated_customer.post(orders_list_url, {}, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Order.objects.count() == 0
    assert "offer_detail_id" in response.data


@pytest.mark.django_db
def test_create_order_requires_valid_offer_detail_id(
    authenticated_customer,
    orders_list_url,
):
    response = authenticated_customer.post(
        orders_list_url,
        {"offer_detail_id": "abc"},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Order.objects.count() == 0
    assert "offer_detail_id" in response.data


@pytest.mark.django_db
def test_create_order_returns_404_for_unknown_offer_detail(
    authenticated_customer,
    orders_list_url,
):
    """Return 404 when the given offer detail does not exist."""
    payload = {"offer_detail_id": 999999}

    response = authenticated_customer.post(orders_list_url, payload, format="json")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Order.objects.count() == 0


@pytest.mark.django_db
def test_create_order_returns_500_when_unexpected_database_error_occurs(
    authenticated_customer,
    orders_list_url,
    offer_detail,
    force_db_crash,
):
    """Return HTTP 500 when an unexpected database error occurs."""
    payload = {"offer_detail_id": offer_detail.id}

    with force_db_crash:
        response = authenticated_customer.post(orders_list_url, payload, format="json")

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

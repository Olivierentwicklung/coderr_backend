import pytest
from django.urls import resolve
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate


@pytest.mark.django_db
def test_list_orders_returns_authenticated_customer_related_orders(
    authenticated_customer,
    orders_list_url,
    customer_order,
    business_order,
    unrelated_order,
):
    """Return only orders connected to the authenticated customer."""
    # Act
    response = authenticated_customer.get(orders_list_url)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

    order_ids = {order["id"] for order in response.data}
    assert customer_order.id in order_ids
    assert business_order.id in order_ids
    assert unrelated_order.id not in order_ids


@pytest.mark.django_db
def test_list_orders_response_contains_expected_fields_and_values(
    authenticated_customer,
    orders_list_url,
    customer_order,
):
    """Return the expected order response fields and values."""
    # Arrange
    expected_fields = {
        "id",
        "customer_user",
        "business_user",
        "title",
        "revisions",
        "delivery_time_in_days",
        "price",
        "features",
        "offer_type",
        "status",
        "created_at",
        "updated_at",
    }

    # Act
    response = authenticated_customer.get(orders_list_url)

    # Assert
    assert response.status_code == status.HTTP_200_OK

    order_data = next(
        order for order in response.data if order["id"] == customer_order.id
    )

    assert set(order_data.keys()) == expected_fields
    assert order_data["customer_user"] == customer_order.customer_user.id
    assert order_data["business_user"] == customer_order.business_user.id
    assert order_data["title"] == customer_order.offer_detail.title
    assert order_data["revisions"] == customer_order.offer_detail.revisions
    assert (
        order_data["delivery_time_in_days"]
        == customer_order.offer_detail.delivery_time_in_days
    )
    assert order_data["price"] == customer_order.offer_detail.price
    assert order_data["features"] == [
        feature.description for feature in customer_order.offer_detail.features.all()
    ]
    assert order_data["offer_type"] == customer_order.offer_detail.offer_type
    assert order_data["status"] == customer_order.status


@pytest.mark.django_db
def test_list_orders_returns_authenticated_business_related_orders(
    authenticated_business,
    orders_list_url,
    customer_order,
    business_order,
    unrelated_order,
):
    """Return only orders connected to the authenticated business user."""
    # Act
    response = authenticated_business.get(orders_list_url)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

    order_ids = {order["id"] for order in response.data}
    assert customer_order.id in order_ids
    assert business_order.id in order_ids
    assert unrelated_order.id not in order_ids


@pytest.mark.django_db
def test_list_orders_requires_authentication(api_client, orders_list_url):
    """Reject unauthenticated users with HTTP 401."""
    # Act
    response = api_client.get(orders_list_url)

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_list_orders_returns_empty_list_when_user_has_no_orders(
    authenticated_customer,
    orders_list_url,
):
    """Return an empty list when the authenticated user has no related orders."""
    # Act
    response = authenticated_customer.get(orders_list_url)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.data == []


@pytest.mark.django_db
def test_list_orders_returns_500_when_unexpected_database_error_occurs(
    authenticated_customer,
    orders_list_url,
    force_db_crash,
):
    """Return HTTP 500 when an unexpected database error occurs."""
    # Act
    with force_db_crash:
        response = authenticated_customer.get(orders_list_url)

    # Assert
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.django_db
@pytest.mark.performance_regression
def test_list_orders_query_count_is_stable(
    django_assert_num_queries,
    orders_list_url,
    customer_user,
    customer_order,
    business_order,
):
    """Avoid query-count regressions for the order list endpoint."""
    # Arrange
    factory = APIRequestFactory()
    request = factory.get(orders_list_url)
    force_authenticate(request, user=customer_user)

    view = resolve(orders_list_url).func

    # Act / Assert
    with django_assert_num_queries(2):
        response = view(request)

    assert response.status_code == status.HTTP_200_OK

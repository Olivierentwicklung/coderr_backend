import pytest
from django.urls import resolve, reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate


@pytest.mark.django_db
def test_update_order_status_as_business_success(
    authenticated_business,
    order_detail_url,
    customer_order,
):
    """Allow a business user to update an order status."""
    payload = {"status": "completed"}

    response = authenticated_business.patch(order_detail_url, payload, format="json")

    customer_order.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert customer_order.status == "completed"

    assert response.data["id"] == customer_order.id
    assert response.data["customer_user"] == customer_order.customer_user.id
    assert response.data["business_user"] == customer_order.business_user.id
    assert response.data["title"] == customer_order.offer_detail.title
    assert response.data["revisions"] == customer_order.offer_detail.revisions
    assert (
        response.data["delivery_time_in_days"]
        == customer_order.offer_detail.delivery_time_in_days
    )
    assert response.data["price"] == customer_order.offer_detail.price
    assert response.data["offer_type"] == customer_order.offer_detail.offer_type
    assert response.data["status"] == "completed"
    assert response.data["features"] == [
        feature.description for feature in customer_order.offer_detail.features.all()
    ]


@pytest.mark.django_db
def test_update_order_status_requires_authentication(
    api_client,
    order_detail_url,
    customer_order,
):
    """Reject unauthenticated users when updating an order status."""
    response = api_client.patch(
        order_detail_url,
        {"status": "completed"},
        format="json",
    )

    customer_order.refresh_from_db()

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert customer_order.status == "in_progress"


@pytest.mark.django_db
def test_update_order_status_requires_business_user(
    authenticated_customer,
    order_detail_url,
    customer_order,
):
    """Reject customer users when updating an order status."""
    response = authenticated_customer.patch(
        order_detail_url,
        {"status": "completed"},
        format="json",
    )

    customer_order.refresh_from_db()

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert customer_order.status == "in_progress"


@pytest.mark.django_db
def test_update_order_status_forbidden_for_unrelated_business(
    api_client,
    second_business_user,
    order_detail_url,
    customer_order,
):
    """Reject business users who are not connected to the order."""
    api_client.force_authenticate(user=second_business_user)

    response = api_client.patch(
        order_detail_url,
        {"status": "completed"},
        format="json",
    )

    customer_order.refresh_from_db()

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert customer_order.status == "in_progress"


@pytest.mark.django_db
def test_update_order_status_rejects_invalid_status(
    authenticated_business,
    order_detail_url,
    customer_order,
):
    """Reject status values outside the allowed choices."""
    response = authenticated_business.patch(
        order_detail_url,
        {"status": "invalid_status"},
        format="json",
    )

    customer_order.refresh_from_db()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert customer_order.status == "in_progress"
    assert "status" in response.data


@pytest.mark.django_db
def test_update_order_status_rejects_unallowed_fields(
    authenticated_business,
    order_detail_url,
    customer_order,
):
    """Reject PATCH requests containing fields other than status."""
    response = authenticated_business.patch(
        order_detail_url,
        {
            "status": "completed",
            "price": 999,
        },
        format="json",
    )

    customer_order.refresh_from_db()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert customer_order.status == "in_progress"


@pytest.mark.django_db
def test_update_order_status_returns_404_for_unknown_order(
    authenticated_business,
):
    """Return 404 when the order does not exist."""
    url = reverse("order-detail", kwargs={"pk": 999999})

    response = authenticated_business.patch(
        url,
        {"status": "completed"},
        format="json",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["detail"] == "The specified order was not found."


@pytest.mark.django_db
def test_update_order_status_returns_500_when_unexpected_database_error_occurs(
    authenticated_business,
    order_detail_url,
    force_db_crash,
):
    """Return HTTP 500 when an unexpected database error occurs."""
    with force_db_crash:
        response = authenticated_business.patch(
            order_detail_url,
            {"status": "completed"},
            format="json",
        )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.django_db
@pytest.mark.performance_regression
def test_update_order_status_query_count_is_stable(
    django_assert_num_queries,
    business_user,
    order_detail_url,
    customer_order,
):
    """Avoid query-count regressions for the order status update endpoint."""
    factory = APIRequestFactory()
    request = factory.patch(
        order_detail_url,
        {"status": "completed"},
        format="json",
    )
    force_authenticate(request, user=business_user)

    view = resolve(order_detail_url).func

    with django_assert_num_queries(3):
        response = view(request, pk=customer_order.pk)

    customer_order.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert customer_order.status == "completed"

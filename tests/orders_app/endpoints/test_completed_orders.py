import pytest
from django.urls import resolve, reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from orders_app.models import Order


@pytest.mark.django_db
def test_completed_order_count_returns_only_completed_orders_for_business_user(
    authenticated_customer,
    completed_order_count_url,
    business_user,
    customer_user,
    second_customer_user,
    offer_detail,
):
    """Verify authenticated users receive only completed orders for the given business user."""
    Order.objects.create(
        customer_user=customer_user,
        business_user=business_user,
        offer_detail=offer_detail,
        status="completed",
    )
    Order.objects.create(
        customer_user=second_customer_user,
        business_user=business_user,
        offer_detail=offer_detail,
        status="completed",
    )
    Order.objects.create(
        customer_user=customer_user,
        business_user=business_user,
        offer_detail=offer_detail,
        status="in_progress",
    )

    response = authenticated_customer.get(completed_order_count_url)

    assert response.status_code == status.HTTP_200_OK
    assert set(response.data.keys()) == {"completed_order_count"}
    assert response.data["completed_order_count"] == 2


@pytest.mark.django_db
def test_completed_order_count_returns_zero_without_completed_orders(
    authenticated_customer,
    completed_order_count_url,
    business_user,
    customer_user,
    offer_detail,
):
    """Verify the endpoint returns zero when no completed orders exist."""
    Order.objects.create(
        customer_user=customer_user,
        business_user=business_user,
        offer_detail=offer_detail,
        status="in_progress",
    )

    response = authenticated_customer.get(completed_order_count_url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"completed_order_count": 0}


@pytest.mark.django_db
def test_completed_order_count_requires_authentication(
    api_client,
    completed_order_count_url,
):
    """Verify unauthenticated users cannot access the completed order count endpoint."""
    response = api_client.get(completed_order_count_url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_completed_order_count_returns_404_for_unknown_business_user(
    authenticated_customer,
):
    """Verify requesting an unknown business user returns a 404 response."""
    url = reverse(
        "completed-order-count",
        kwargs={"business_user_id": 999999},
    )

    response = authenticated_customer.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_completed_order_count_returns_404_for_non_business_user(
    authenticated_customer,
    customer_user,
):
    """Verify requesting a non-business user returns a 404 response."""
    url = reverse(
        "completed-order-count",
        kwargs={"business_user_id": customer_user.pk},
    )

    response = authenticated_customer.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_completed_order_count_returns_500_on_unexpected_database_error(
    authenticated_customer,
    completed_order_count_url,
    force_db_crash,
):
    """Verify unexpected database errors are returned as HTTP 500 responses."""
    with force_db_crash:
        response = authenticated_customer.get(completed_order_count_url)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.django_db
def test_completed_order_count_query_count(
    django_assert_num_queries,
    business_user,
    customer_user,
    second_customer_user,
    offer_detail,
):
    """Verify the completed order count endpoint query count does not regress."""
    Order.objects.create(
        customer_user=customer_user,
        business_user=business_user,
        offer_detail=offer_detail,
        status="completed",
    )
    Order.objects.create(
        customer_user=second_customer_user,
        business_user=business_user,
        offer_detail=offer_detail,
        status="completed",
    )
    Order.objects.create(
        customer_user=customer_user,
        business_user=business_user,
        offer_detail=offer_detail,
        status="in_progress",
    )

    url = reverse(
        "completed-order-count",
        kwargs={"business_user_id": business_user.pk},
    )
    request = APIRequestFactory().get(url)
    force_authenticate(request, user=customer_user)
    view = resolve(url).func

    with django_assert_num_queries(2):
        response = view(request, business_user_id=business_user.pk)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"completed_order_count": 2}

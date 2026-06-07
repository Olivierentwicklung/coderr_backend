import pytest
from django.urls import resolve, reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from orders_app.models import Order


@pytest.mark.django_db
def test_delete_order_as_staff_success(
    authenticated_staff,
    order_detail_url,
    customer_order,
):
    """Allow staff users to delete an order."""
    response = authenticated_staff.delete(order_detail_url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data is None
    assert not Order.objects.filter(pk=customer_order.pk).exists()


@pytest.mark.django_db
def test_delete_order_requires_authentication(
    api_client,
    order_detail_url,
    customer_order,
):
    """Reject unauthenticated users when deleting an order."""
    response = api_client.delete(order_detail_url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Order.objects.filter(pk=customer_order.pk).exists()


@pytest.mark.django_db
def test_delete_order_requires_staff_user(
    authenticated_business,
    order_detail_url,
    customer_order,
):
    """Reject non-staff users when deleting an order."""
    response = authenticated_business.delete(order_detail_url)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Order.objects.filter(pk=customer_order.pk).exists()


@pytest.mark.django_db
def test_delete_order_returns_404_for_unknown_order(authenticated_staff):
    """Return 404 when deleting an unknown order."""
    url = reverse("order-detail", kwargs={"pk": 999999})

    response = authenticated_staff.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_order_returns_500_when_unexpected_database_error_occurs(
    authenticated_staff,
    order_detail_url,
    force_db_crash,
):
    """Return HTTP 500 when an unexpected database error occurs."""
    with force_db_crash:
        response = authenticated_staff.delete(order_detail_url)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.django_db
@pytest.mark.performance_regression
def test_delete_order_query_count_is_stable(
    django_assert_num_queries,
    staff_user,
    order_detail_url,
    customer_order,
):
    """Avoid query-count regressions for deleting an order."""
    factory = APIRequestFactory()
    request = factory.delete(order_detail_url)
    force_authenticate(request, user=staff_user)

    view = resolve(order_detail_url).func

    with django_assert_num_queries(3):
        response = view(request, pk=customer_order.pk)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Order.objects.filter(pk=customer_order.pk).exists()

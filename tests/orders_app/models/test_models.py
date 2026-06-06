import pytest
from django.contrib.auth import get_user_model

from offers_app.models import Offer, OfferDetail
from orders_app.models import Order


@pytest.fixture
def customer_user():
    User = get_user_model()

    return User.objects.create_user(  # type: ignore[attr-defined]
        username="customer1",
        email="customer@test.com",
        password="testpass123",
        type="customer",
    )


@pytest.fixture
def business_user():
    User = get_user_model()

    return User.objects.create_user(  # type: ignore[attr-defined]
        username="business1",
        email="business@test.com",
        password="testpass123",
        type="business",
    )


@pytest.fixture
def offer_detail(business_user):
    offer = Offer.objects.create(
        business_user=business_user,
        title="Logo Design",
        description="Professional logo design",
    )

    return OfferDetail.objects.create(
        offer=offer,
        title="Basic Package",
        revisions=2,
        delivery_time_in_days=3,
        price=100,
        offer_type="basic",
    )


@pytest.mark.django_db
def test_create_order(customer_user, business_user, offer_detail):
    order = Order.objects.create(
        customer_user=customer_user,
        business_user=business_user,
        offer_detail=offer_detail,
        status="in_progress",
    )

    assert order.customer_user == customer_user
    assert order.business_user == business_user
    assert order.offer_detail == offer_detail
    assert order.status == "in_progress"


@pytest.mark.django_db
def test_order_default_status(customer_user, business_user, offer_detail):
    order = Order.objects.create(
        customer_user=customer_user,
        business_user=business_user,
        offer_detail=offer_detail,
    )

    assert order.status == "in_progress"


@pytest.mark.django_db
def test_order_string_representation(customer_user, business_user, offer_detail):
    order = Order.objects.create(
        customer_user=customer_user,
        business_user=business_user,
        offer_detail=offer_detail,
    )

    assert str(order) == f"Order #{order.id}"  # type:ignore

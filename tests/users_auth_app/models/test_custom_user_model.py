import pytest
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_create_customer_user():
    User = get_user_model()

    user = User.objects.create_user(  # type: ignore[attr-defined]
        username="customer1",
        email="customer@test.com",
        password="testpass123",
        type="customer",
    )

    assert user.username == "customer1"
    assert user.email == "customer@test.com"
    assert user.type == "customer"
    assert user.check_password("testpass123")


@pytest.mark.django_db
def test_create_business_user():
    User = get_user_model()

    user = User.objects.create_user(  # type: ignore
        username="business1",
        email="business@test.com",
        password="testpass123",
        type="business",
    )

    assert user.type == "business"


@pytest.mark.django_db
def test_custom_user_string_representation():
    User = get_user_model()

    user = User.objects.create_user(  # type: ignore
        username="customer1",
        email="customer@test.com",
        password="testpass123",
        type="customer",
    )

    assert str(user) == "customer1"

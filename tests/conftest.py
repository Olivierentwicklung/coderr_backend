import pytest
from django.contrib.auth import get_user_model
from django.db import connection
from django.db.utils import OperationalError
from django.urls import reverse
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    """Return DRF API client."""
    client = APIClient()
    client.raise_request_exception = False  # Only for Testing 500
    return client


class ForceDatabaseCrashWrapper:
    """A clean interceptor that forces any SQL execution to crash instantly."""

    def __call__(self, execute, sql, params, many, context):
        raise OperationalError("Unexpected database error")


@pytest.fixture
def force_db_crash():
    """
    Fixture to force all database queries to fail within its context.
    This wraps the entire request execution block, forcing a 500 status response
    """
    return connection.execute_wrapper(ForceDatabaseCrashWrapper())


@pytest.fixture
def registration_url():
    """Return the registration endpoint URL."""
    return reverse("registration")


@pytest.fixture
def customer_user():
    """Create a customer user."""
    return User.objects.create_user(  # type:ignore
        username="customer",
        email="customer@test.com",
        password="testpassword123",
        type="customer",
    )


@pytest.fixture
def business_user():
    """Create a business user."""
    return User.objects.create_user(  # type:ignore
        username="business",
        email="business@test.com",
        password="testpassword123",
        type="business",
        first_name="Max",
        last_name="Mustermann",
        location="Berlin",
        tel="123456789",
        description="Business description",
        working_hours="9-17",
    )


@pytest.fixture
def valid_registration_payload():
    """Valid registration payload."""
    return {
        "username": "exampleUsername",
        "email": "example@mail.de",
        "password": "examplePassword",
        "repeated_password": "examplePassword",
        "type": "customer",
    }


@pytest.fixture
def login_url():
    """Return login endpoint URL."""
    return reverse("login")


@pytest.fixture
def valid_login_custom_user_payload(customer_user):
    """Return valid login payload."""
    return {
        "username": customer_user.username,
        "password": "testpassword123",
    }


@pytest.fixture
def valid_login_business_user_payload(business_user):
    """Return valid login payload."""
    return {
        "username": business_user.username,
        "password": "testpassword123",
    }


@pytest.fixture
def profile_detail_url(business_user):
    """Return profile detail endpoint URL."""
    return reverse("profile-detail", kwargs={"pk": business_user.id})


@pytest.fixture
def authenticated_customer(api_client, customer_user):
    """Return authenticated API client as customer."""
    api_client.force_authenticate(user=customer_user)
    return api_client


@pytest.fixture
def authenticated_business(api_client, business_user):
    """Return authenticated API client as business."""
    api_client.force_authenticate(user=business_user)
    return api_client

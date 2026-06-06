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

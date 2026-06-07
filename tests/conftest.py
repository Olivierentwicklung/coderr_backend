import pytest
from django.contrib.auth import get_user_model
from django.db import connection
from django.db.utils import OperationalError
from django.urls import reverse
from rest_framework.test import APIClient

from offers_app.models import Offer, OfferDetail

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
def second_customer_user():
    """Create and return a second customer user."""
    return User.objects.create_user(  # type:ignore
        username="customer_jane",
        email="customer_jane@test.com",
        password="testpassword123",
        type="customer",
        first_name="Jane",
        last_name="Doe",
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
def second_business_user():
    """Create and return a second business user."""
    return User.objects.create_user(  # type:ignore
        username="second_business",
        email="second_business@test.com",
        password="testpassword123",
        type="business",
        first_name="Second",
        last_name="Business",
        location="Hamburg",
        tel="222333444",
        description="Second business description",
        working_hours="8-16",
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


@pytest.fixture
def profile_update_url(business_user):
    """Return profile update endpoint URL."""
    return reverse("profile-detail", kwargs={"pk": business_user.id})


@pytest.fixture
def valid_profile_update_payload():
    """Return valid profile update payload."""
    return {
        "first_name": "Max",
        "last_name": "Mustermann",
        "location": "Berlin",
        "tel": "987654321",
        "description": "Updated business description",
        "working_hours": "10-18",
        "email": "new_email@business.de",
    }


@pytest.fixture
def business_profiles_url():
    """Return business profiles list endpoint URL."""
    return reverse("business-profiles")


@pytest.fixture
def customer_profiles_url():
    """Return customer profiles list endpoint URL."""
    return reverse("customer-profiles")


@pytest.fixture
def offers_list_url():
    """Return the offers list endpoint URL."""
    return reverse("offer-list")


@pytest.fixture
def offer(business_user):
    """Create an offer with multiple details."""
    offer = Offer.objects.create(
        business_user=business_user,
        title="Website Design",
        description="Professionelles Website-Design",
    )

    OfferDetail.objects.create(
        offer=offer,
        title="Basic",
        revisions=1,
        delivery_time_in_days=7,
        price=100,
        offer_type="basic",
    )

    OfferDetail.objects.create(
        offer=offer,
        title="Standard",
        revisions=3,
        delivery_time_in_days=10,
        price=200,
        offer_type="standard",
    )

    OfferDetail.objects.create(
        offer=offer,
        title="Premium",
        revisions=5,
        delivery_time_in_days=14,
        price=300,
        offer_type="premium",
    )

    return offer


@pytest.fixture
def second_offer(second_business_user):
    """Create a second offer."""
    offer = Offer.objects.create(
        business_user=second_business_user,
        title="Logo Design",
        description="Modern branding package",
    )

    OfferDetail.objects.create(
        offer=offer,
        title="Basic",
        revisions=1,
        delivery_time_in_days=3,
        price=50,
        offer_type="basic",
    )

    return offer


@pytest.fixture
def offer_create_payload():
    """Return valid offer creation payload with exactly three details."""
    return {
        "title": "Grafikdesign-Paket",
        "image": None,
        "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
        "details": [
            {
                "title": "Basic Design",
                "revisions": 2,
                "delivery_time_in_days": 5,
                "price": 100,
                "features": ["Logo Design", "Visitenkarte"],
                "offer_type": "basic",
            },
            {
                "title": "Standard Design",
                "revisions": 5,
                "delivery_time_in_days": 7,
                "price": 200,
                "features": ["Logo Design", "Visitenkarte", "Briefpapier"],
                "offer_type": "standard",
            },
            {
                "title": "Premium Design",
                "revisions": 10,
                "delivery_time_in_days": 10,
                "price": 500,
                "features": ["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"],
                "offer_type": "premium",
            },
        ],
    }

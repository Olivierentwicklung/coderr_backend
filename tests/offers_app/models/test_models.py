import pytest
from django.contrib.auth import get_user_model

from offers_app.models import Offer, OfferDetail, OfferDetailFeature
from uploads_app.models import FileUpload


@pytest.fixture
def business_user():
    User = get_user_model()

    return User.objects.create_user(  # type: ignore
        username="business1",
        email="business@test.com",
        password="testpass123",
        type="business",
    )


@pytest.fixture
def image(business_user):
    return FileUpload.objects.create(
        file="uploads/offer.png",
        uploaded_by=business_user,
    )


@pytest.fixture
def offer(business_user, image):
    return Offer.objects.create(
        business_user=business_user,
        title="Logo Design",
        description="Professional logo design",
        image=image,
    )


@pytest.fixture
def offer_detail(offer):
    return OfferDetail.objects.create(
        offer=offer,
        title="Basic Package",
        revisions=2,
        delivery_time_in_days=3,
        price=100,
        offer_type="basic",
    )


@pytest.mark.django_db
def test_create_offer(business_user, image):
    offer = Offer.objects.create(
        business_user=business_user,
        title="Logo Design",
        description="Professional logo design",
        image=image,
    )

    assert offer.business_user == business_user
    assert offer.title == "Logo Design"
    assert offer.description == "Professional logo design"
    assert offer.image == image


@pytest.mark.django_db
def test_offer_string_representation(offer):
    assert str(offer) == "Logo Design"


@pytest.mark.django_db
def test_create_offer_detail(offer):
    detail = OfferDetail.objects.create(
        offer=offer,
        title="Basic Package",
        revisions=2,
        delivery_time_in_days=3,
        price=100,
        offer_type="basic",
    )

    assert detail.offer == offer
    assert detail.title == "Basic Package"
    assert detail.revisions == 2
    assert detail.delivery_time_in_days == 3
    assert detail.price == 100
    assert detail.offer_type == "basic"


@pytest.mark.django_db
def test_offer_detail_string_representation(offer_detail):
    assert str(offer_detail) == "Logo Design - Basic Package"


@pytest.mark.django_db
def test_create_offer_detail_feature(offer_detail):
    feature = OfferDetailFeature.objects.create(
        offer_detail=offer_detail,
        description="1 logo concept",
    )

    assert feature.offer_detail == offer_detail
    assert feature.description == "1 logo concept"


@pytest.mark.django_db
def test_offer_detail_feature_string_representation(offer_detail):
    feature = OfferDetailFeature.objects.create(
        offer_detail=offer_detail,
        description="1 logo concept",
    )

    assert str(feature) == "1 logo concept"

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from reviews_app.models import Review


@pytest.fixture
def reviewer():
    User = get_user_model()

    return User.objects.create_user(  # type: ignore
        username="customer1",
        email="customer@test.com",
        password="testpass123",
        type="customer",
    )


@pytest.fixture
def business_user():
    User = get_user_model()

    return User.objects.create_user(  # type: ignore
        username="business1",
        email="business@test.com",
        password="testpass123",
        type="business",
    )


@pytest.mark.django_db
def test_create_review_for_business_user(reviewer, business_user):
    review = Review.objects.create(
        reviewer=reviewer,
        business_user=business_user,
        rating=4,
        description="Everything was great!",
    )

    assert review.reviewer == reviewer
    assert review.business_user == business_user
    assert review.rating == 4
    assert review.description == "Everything was great!"


@pytest.mark.django_db
def test_review_string_representation(reviewer, business_user):
    review = Review.objects.create(
        reviewer=reviewer,
        business_user=business_user,
        rating=4,
        description="Everything was great!",
    )

    assert str(review) == "4 stars for business1"


@pytest.mark.django_db
def test_review_rating_cannot_be_lower_than_one(reviewer, business_user):
    review = Review(
        reviewer=reviewer,
        business_user=business_user,
        rating=0,
        description="Invalid rating",
    )

    with pytest.raises(ValidationError):
        review.full_clean()


@pytest.mark.django_db
def test_review_rating_cannot_be_higher_than_five(reviewer, business_user):
    review = Review(
        reviewer=reviewer,
        business_user=business_user,
        rating=6,
        description="Invalid rating",
    )

    with pytest.raises(ValidationError):
        review.full_clean()


@pytest.mark.django_db
def test_reviewer_can_review_business_user_only_once(reviewer, business_user):
    Review.objects.create(
        reviewer=reviewer,
        business_user=business_user,
        rating=5,
        description="Great work!",
    )

    with pytest.raises(IntegrityError):
        Review.objects.create(
            reviewer=reviewer,
            business_user=business_user,
            rating=4,
            description="Second review",
        )

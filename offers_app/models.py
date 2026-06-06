from django.conf import settings
from django.db import models


class Offer(models.Model):
    """
    Represents a service offer created by a business user.

    An offer can contain multiple offer details such as basic,
    standard, and premium packages.
    """

    business_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="offers",
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ForeignKey(
        "uploads_app.FileUpload",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="offer_images",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Return the offer title as the readable string representation.
        """
        return self.title


class OfferDetail(models.Model):
    """
    Represents a package option for an offer.

    Each offer detail belongs to one offer and defines price,
    revisions, delivery time, and package type.
    """

    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"

    OFFER_TYPE_CHOICES = [
        (BASIC, "Basic"),
        (STANDARD, "Standard"),
        (PREMIUM, "Premium"),
    ]

    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name="details",
    )
    title = models.CharField(max_length=255)
    revisions = models.PositiveIntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPE_CHOICES)

    def __str__(self):
        """
        Return the offer title and package title as readable text.
        """
        return f"{self.offer.title} - {self.title}"


class OfferDetailFeature(models.Model):
    """
    Represents a single feature of an offer detail package.

    Example: one logo concept, source file included, or fast delivery.
    """

    offer_detail = models.ForeignKey(
        OfferDetail,
        on_delete=models.CASCADE,
        related_name="features",
    )
    description = models.CharField(max_length=255)

    def __str__(self):
        """
        Return the feature description as readable text.
        """
        return self.description

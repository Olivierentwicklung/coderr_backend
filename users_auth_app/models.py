from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    CUSTOMER = "customer"
    BUSINESS = "business"

    USER_TYPE_CHOICES = [
        (CUSTOMER, "Customer"),
        (BUSINESS, "Business"),
    ]

    email = models.EmailField(unique=True)
    type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    profile_file = models.ForeignKey(
        "uploads_app.FileUpload",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profile_users",
    )

    def __str__(self):
        return self.username

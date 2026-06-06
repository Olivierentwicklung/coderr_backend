import pytest
from django.contrib.auth import get_user_model

from uploads_app.models import FileUpload


@pytest.mark.django_db
def test_create_file_upload():
    User = get_user_model()

    user = User.objects.create_user(  # type: ignore
        username="user1",
        email="user1@test.com",
        password="testpass123",
        type="customer",
    )

    upload = FileUpload.objects.create(
        file="uploads/test.png",
        uploaded_by=user,
    )

    assert upload.file == "uploads/test.png"
    assert upload.uploaded_by == user


@pytest.mark.django_db
def test_file_upload_string_representation():
    User = get_user_model()

    user = User.objects.create_user(  # type: ignore
        username="user1",
        email="user1@test.com",
        password="testpass123",
        type="customer",
    )

    upload = FileUpload.objects.create(
        file="uploads/test.png",
        uploaded_by=user,
    )

    assert str(upload) == "uploads/test.png"

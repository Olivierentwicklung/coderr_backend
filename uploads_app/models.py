from django.conf import settings
from django.db import models


class FileUpload(models.Model):
    """
    Stores uploaded files that can be reused by different apps.

    A file upload belongs to the user who uploaded it.
    """

    file = models.FileField(upload_to="uploads/")
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uploads",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return the stored file path as the readable string representation.
        """
        return str(self.file)

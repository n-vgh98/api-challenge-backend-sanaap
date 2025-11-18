from accounts.models import User

from django.db import models


class FileObject(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_documents",
    )
    file_name = models.CharField(max_length=255)
    file_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):

        return f"{self.file_name}"

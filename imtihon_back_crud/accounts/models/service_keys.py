# models.py

from django.db import models
import secrets


class APIKey(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the client or service")
    key = models.CharField(max_length=64, unique=True, editable=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = secrets.token_hex(32)  # Generates a 64-char hex key
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {'active' if self.is_active else 'inactive'}"

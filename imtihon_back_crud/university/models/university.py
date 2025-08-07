from django.db import models
from django.conf import settings


# Create your models here.
class UniversityModel(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="university",
        null=True,
        blank=True,  # optional if you want to create without user
    )

    name = models.CharField(max_length=255)  # required

    location = models.CharField(max_length=255, blank=True, null=True)
    longtitude = models.CharField(blank=True, null=True)
    latitude = models.CharField(blank=True, null=True)

    number = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name

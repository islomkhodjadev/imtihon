from django.db import models
from django.conf import settings
from university.models import UniversityModel, DepartmentModel


class SubjectModel(models.Model):
    university = models.ForeignKey(
        UniversityModel, on_delete=models.CASCADE, related_name="subjects"
    )
    department = models.ForeignKey(
        DepartmentModel, on_delete=models.CASCADE, related_name="subjects"
    )
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"university: {self.university.name} subject:{self.name}"

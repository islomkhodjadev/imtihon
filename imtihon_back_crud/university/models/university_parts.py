from django.db import models
from django.conf import settings
from university.models import UniversityModel


class FacultyModel(models.Model):
    university = models.ForeignKey(
        UniversityModel, on_delete=models.CASCADE, related_name="faculties"
    )
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"University: {self.university.name} - faculty: {self.name}"


class DepartmentModel(models.Model):
    faculty = models.ForeignKey(FacultyModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    code = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"university:{self.faculty.university.name} - group:{self.name}"


class GroupModel(models.Model):
    university = models.ForeignKey(
        UniversityModel, on_delete=models.CASCADE, related_name="groups"
    )
    department = models.ForeignKey(
        DepartmentModel, on_delete=models.CASCADE, related_name="groups"
    )
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"university: {self.university.name} - group:{self.name}"

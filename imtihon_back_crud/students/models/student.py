from django.db import models
from django.conf import settings
from university.models import UniversityModel, GroupModel

# Create your models here.


class StudentProfileModel(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        unique=True,
        related_name="student_profile",
    )

    student_id_number = models.CharField(max_length=50, unique=True)
    image_url = models.URLField()

    # New fields
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100, blank=True, null=True)
    third_name = models.CharField(max_length=100, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    short_name = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    passport_pin = models.CharField(max_length=20, blank=True, null=True)
    passport_number = models.CharField(max_length=20, blank=True, null=True)

    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    gender_code = models.CharField(max_length=10, blank=True, null=True)
    gender_name = models.CharField(max_length=20, blank=True, null=True)

    university = models.ForeignKey(
        UniversityModel, on_delete=models.CASCADE, related_name="student_profiles"
    )

    department = models.CharField(max_length=100, blank=True, null=True)
    year_of_study = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"university : {self.university.name} - student_id : {self.student_id_number}"


class StudentsGroupModel(models.Model):
    student = models.ForeignKey(
        StudentProfileModel, on_delete=models.CASCADE, related_name="groups"
    )
    group = models.ForeignKey(
        GroupModel, on_delete=models.CASCADE, related_name="students"
    )

    def __str__(self) -> str:
        return f"{self.group} - student: {self.student.student_id_number}"

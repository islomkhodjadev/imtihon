from django.db import models
from django.conf import settings
from university.models import UniversityModel, SubjectModel


class ProfessorProfileModel(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        unique=True,
        related_name="professor_profile",
    )
    university = models.ForeignKey(
        UniversityModel, on_delete=models.CASCADE, related_name="professor_profiles"
    )
    professor_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"university: {self.university.name} - professor_name:{self.name} "


class ProfessorsSubjectModel(models.Model):
    professor = models.ForeignKey(
        ProfessorProfileModel,
        on_delete=models.CASCADE,
        related_name="professor_subjects",
    )
    subject = models.ForeignKey(
        SubjectModel, on_delete=models.CASCADE, related_name="professors"
    )

    def __str__(self):
        return f"{self.professor} - subject:{self.subject.name}"

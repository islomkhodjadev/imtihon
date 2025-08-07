from django.db import models
from students.models import StudentProfileModel
from university.models import SubjectModel


class StudentSubjectModel(models.Model):
    student = models.ForeignKey(
        StudentProfileModel, on_delete=models.CASCADE, related_name="subjects"
    )
    subject = models.ForeignKey(
        SubjectModel, on_delete=models.CASCADE, related_name="students"
    )

from typing import Any
from django.db import models
from university.models import SubjectModel, GroupModel
from professors.models import ProfessorProfileModel


class AssignmentModel(models.Model):

    type_choices = [
        ("hw", "homework"),
        ("exam", "exam"),
        ("project", "project"),
        ("quiz", "quiz"),
    ]

    subject = models.ForeignKey(
        SubjectModel, on_delete=models.CASCADE, related_name="assignments"
    )
    professor = models.ForeignKey(
        ProfessorProfileModel, on_delete=models.CASCADE, related_name="assignments"
    )
    type = models.CharField(choices=type_choices, max_length=20)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    description = models.TextField()

    max_grade = models.IntegerField()

    def __str__(self) -> str:
        return (
            f"{self.get_type_display().capitalize()} | "
            f"Subject: {self.subject.name} | "
            f"Prof: {self.professor.professor_id} | "
            f"{self.start_time.strftime('%Y-%m-%d')}"
        )


class AssignmentAttachmentsModel(models.Model):
    assignment = models.ForeignKey(
        AssignmentModel, on_delete=models.CASCADE, related_name="attachments"
    )
    attachment_file = models.FileField()

    def __str__(self) -> str:
        return f"attachment for assignment: {self.assignment.id}"


class AssignmentsGroupModel(models.Model):
    assignment = models.ForeignKey(
        AssignmentModel, on_delete=models.CASCADE, related_name="groups"
    )
    group = models.ForeignKey(
        GroupModel, on_delete=models.CASCADE, related_name="assignment_groups"
    )

    def __str__(self) -> str:
        return f"{self.assignment} - {self.group}"

    class Meta:
        unique_together = ("assignment", "group")

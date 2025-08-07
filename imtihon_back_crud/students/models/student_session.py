from django.db import models
from students.models import StudentProfileModel
from assignments.models import AssignmentModel, QuestionModel, QuestionChoiceModel


# // student assignment taking
# student_session:
#   - id
#   - student_id
#   - assignment_id
#   - start_time
#   - end_time
#   - cheating_score
#   - grade


class StudentSessionModel(models.Model):
    student = models.ForeignKey(
        StudentProfileModel, on_delete=models.CASCADE, related_name="sessions"
    )
    assignment = models.ForeignKey(
        AssignmentModel, on_delete=models.CASCADE, related_name="student_sessions"
    )
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    cheating_score = models.IntegerField(null=True, blank=True)
    grade = models.IntegerField(null=True, blank=True)
    is_live = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"session: {self.id} of student: {self.student.id}"


class CheatingEvidenceModel(models.Model):
    type_choices = [
        ("device", "device"),
        ("multiple_people", "multiple_people"),
        ("audio", "audio"),
        ("ai", "ai"),
        ("tab_switch", "Tab switch"),
    ]

    session = models.ForeignKey(
        StudentSessionModel, on_delete=models.CASCADE, related_name="cheating_evidence"
    )
    type = models.CharField(max_length=20, choices=type_choices)
    evidence_file = models.FileField()

    def __str__(self) -> str:
        return f"id: {self.id}: {self.session} type: {self.type}"


class StudentAnswerModel(models.Model):
    session = models.ForeignKey(
        StudentSessionModel, on_delete=models.CASCADE, related_name="answers"
    )
    question = models.ForeignKey(
        QuestionModel, on_delete=models.CASCADE, related_name="student_answers"
    )
    text_answer = models.TextField(null=True, blank=True)

    choice = models.ForeignKey(
        QuestionChoiceModel,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="student_answers",
    )

    true_false_answer = models.BooleanField(null=True, blank=True)

    def __str__(self) -> str:
        return f"id: {self.id} - {self.session}"

    class Meta:
        unique_together = ("session", "question")

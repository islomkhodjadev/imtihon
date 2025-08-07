from django.db import models
from assignments.models import AssignmentModel


class QuestionModel(models.Model):
    type_choices = [
        ("mcq", "multiple choice question"),
        ("open", "open question"),
        ("true_false", "true or false question"),
    ]

    assignment = models.ForeignKey(
        AssignmentModel, on_delete=models.CASCADE, related_name="questions"
    )
    question = models.TextField()
    text_answer = models.TextField(null=True, blank=True)
    true_false_answer = models.BooleanField(null=True, blank=True)
    type = models.CharField(max_length=10, choices=type_choices)

    def __str__(self) -> str:
        preview = self.question[:40] + ("..." if len(self.question) > 40 else "")
        return f"Assignment: {self.assignment.id} | Type: {self.type} | Q: {preview}"


class QuestionChoiceModel(models.Model):
    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE)
    choice = models.TextField()
    is_correct = models.BooleanField()

    def __str__(self) -> str:
        preview = self.choice[:30] + ("..." if len(self.choice) > 30 else "")
        return f"Q: {self.question.id} | Choice: {preview} | Correct: {self.is_correct}"

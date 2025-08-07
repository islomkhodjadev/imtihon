from django.db import models
from university.models import GroupModel, SubjectModel
from professors.models import ProfessorProfileModel


class StudentTimetableModel(models.Model):
    group = models.ForeignKey(
        GroupModel, on_delete=models.CASCADE, related_name="student_timetables"
    )

    def __str__(self) -> str:
        return f"{self.group}"


class StudentTimeTablesubjectModel(models.Model):
    day_choices = [
        ("monday", "monday"),
        ("tuesday", "tuesday"),
        ("wednesday", "wednesday"),
        ("thursday", "thursday"),
        ("friday", "friday"),
        ("saturday", "saturday"),
        ("sunday", "sunday"),
    ]

    timetable = models.ForeignKey(
        StudentTimetableModel, on_delete=models.CASCADE, related_name="subjects"
    )

    subject = models.ForeignKey(
        SubjectModel, on_delete=models.CASCADE, related_name="subjects"
    )
    professor = models.ForeignKey(
        ProfessorProfileModel, on_delete=models.CASCADE, related_name="timetable_subjects"
    )

    day = models.CharField(choices=day_choices, max_length=10)

    start_time = models.TimeField()
    end_time = models.TimeField()

    room = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.subject.name

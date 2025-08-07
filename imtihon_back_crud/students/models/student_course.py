from django.db import models
from course.models import CourseModel, CourseLessonModel
from students.models import StudentProfileModel


class StudentCourseModel(models.Model):
    course = models.ForeignKey(
        CourseModel, on_delete=models.CASCADE, related_name="student_courses"
    )
    student = models.ForeignKey(
        StudentProfileModel, on_delete=models.CASCADE, related_name="courses"
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(null=True, blank=True)
    grade = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f"student_id: {self.student} course: {self.course.name}"


class StudentCourseProgressModel(models.Model):
    student_course = models.ForeignKey(
        StudentCourseModel, on_delete=models.CASCADE, related_name="progresses"
    )
    lesson = models.ForeignKey(
        CourseLessonModel, on_delete=models.CASCADE, related_name="student_progresses"
    )
    is_completed = models.BooleanField()

    def __str__(self) -> str:
        return f"{self.student_course} lesson: {self.lesson}"

    class Meta:
        unique_together = ("student_course", "lesson")

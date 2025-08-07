from django.db import models
from university.models import UniversityModel, SubjectModel
from professors.models import ProfessorProfileModel


class CourseModel(models.Model):
    subject = models.ForeignKey(
        SubjectModel, on_delete=models.CASCADE, related_name="courses"
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    intro_image = models.ImageField(
        upload_to="uploads/course/%Y/%m/%d/", null=True, blank=True
    )

    def __str__(self) -> str:
        return f"id: {self.id} name: {self.name}"


class CourseSectionModel(models.Model):
    course = models.ForeignKey(
        CourseModel, on_delete=models.CASCADE, related_name="sections"
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    intro_video = models.FileField(
        upload_to="uploads/course_section/video/%Y/%m/%d/", null=True, blank=True
    )
    intro_image = models.ImageField(
        upload_to="uploads/course_section/video/%Y/%m/%d/", null=True, blank=True
    )

    def __str__(self) -> str:
        return f"course: {self.course.name} - section: {self.name}"


class CourseLessonModel(models.Model):
    section = models.ForeignKey(
        CourseSectionModel, on_delete=models.CASCADE, related_name="lessons"
    )
    name = models.CharField(max_length=255)
    text = models.TextField()
    video = models.FileField(
        upload_to="uploads/course_lesson/video/%Y/%m/%d/", null=True, blank=True
    )
    image = models.ImageField(
        upload_to="uploads/course_lesson/image/%Y/%m/%d/", null=True, blank=True
    )

    def __str__(self) -> str:
        return f"course: {self.section.course.name} - lesson: {self.name}"


# adding attachement to course lesson


class CourseAttachmentsModel(models.Model):
    course = models.ForeignKey(
        CourseModel, on_delete=models.CASCADE, related_name="course_attachments"
    )
    attachment_file = models.FileField()

    def __str__(self) -> str:
        return f"attachment for course: {self.course.id}"

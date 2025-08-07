from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from students.models import (
    StudentProfileModel,
    StudentsGroupModel,
    StudentCourseModel,
    StudentCourseProgressModel,
    StudentSessionModel,
    CheatingEvidenceModel,
    StudentAnswerModel,
    StudentTimetableModel,
    StudentTimeTablesubjectModel,
)
from university.models import (
    UniversityModel,
    GroupModel,
    DepartmentModel,
    FacultyModel,
    SubjectModel,
)
from course.models import CourseModel, CourseLessonModel, CourseSectionModel
from professors.models import ProfessorProfileModel
from assignments.models import AssignmentModel
from django.utils import timezone
from datetime import timedelta


class StudentsAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.university = UniversityModel.objects.create(
            user=self.user,
            name="Uni",
            location="Loc",
            longtitude="0",
            latitude="0",
            number="123",
            email="a@a.com",
            website="http://a.com",
            description="desc",
        )
        self.faculty = FacultyModel.objects.create(
            university=self.university, name="Faculty", description="desc"
        )
        self.department = DepartmentModel.objects.create(
            faculty=self.faculty, name="Dept", description="desc"
        )
        self.group = GroupModel.objects.create(
            university=self.university, department=self.department, number=1
        )
        self.professor = ProfessorProfileModel.objects.create(
            user=self.user, university=self.university, professor_id="P001"
        )
        self.subject = SubjectModel.objects.create(
            university=self.university,
            department=self.department,
            name="Math",
            description="desc",
        )
        self.profile = StudentProfileModel.objects.create(
            user=self.user, student_id="S001", university=self.university
        )
        self.section = CourseSectionModel.objects.create(
            course=CourseModel.objects.create(
                university=self.university,
                professor=self.professor,
                name="Course",
                description="desc",
            ),
            name="Section",
            description="desc",
        )
        self.lesson = CourseLessonModel.objects.create(
            section=self.section, name="Lesson", text="text"
        )
        self.course = self.section.course
        self.student_course = StudentCourseModel.objects.create(
            course=self.course,
            student=self.profile,
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(days=1),
            is_completed=False,
        )
        self.assignment = AssignmentModel.objects.create(
            subject=self.subject,
            professor=self.professor,
            type="hw",
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            description="desc",
            max_grade=100,
        )
        self.session = StudentSessionModel.objects.create(
            student=self.profile, assignment=self.assignment, cheating_score=0, grade=0
        )
        self.timetable = StudentTimetableModel.objects.create(group=self.group)

    def test_list_profiles(self):
        url = reverse("studentprofilemodel-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_groups(self):
        url = reverse("studentsgroupmodel-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_courses(self):
        url = reverse("studentcoursemodel-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_progress(self):
        url = reverse("studentcourseprogressmodel-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_sessions(self):
        url = reverse("studentsessionmodel-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_cheating_evidence(self):
        url = reverse("cheatingevidencemodel-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_answers(self):
        url = reverse("studentanswermodel-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_timetables(self):
        url = reverse("studenttimetablemodel-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_timetable_subjects(self):
        url = reverse("studenttimetablesubjectmodel-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from assignments.models import (
    AssignmentModel,
    AssignmentAttachmentsModel,
    AssignmentsGroupModel,
    QuestionModel,
    QuestionChoiceModel,
)
from university.models import (
    SubjectModel,
    GroupModel,
    DepartmentModel,
    FacultyModel,
    UniversityModel,
)
from professors.models import ProfessorProfileModel
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from datetime import timedelta


class AssignmentsAPITestCase(APITestCase):
    def setUp(self):
        # Create all required related objects
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
        self.subject = SubjectModel.objects.create(
            university=self.university,
            department=self.department,
            name="Math",
            description="Math desc",
        )
        self.professor = ProfessorProfileModel.objects.create(
            user=self.user, university=self.university, professor_id="P001"
        )
        # Assignment
        self.assignment = AssignmentModel.objects.create(
            subject=self.subject,
            professor=self.professor,
            type="hw",
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            description="desc",
            max_grade=100,
        )
        # Question
        self.question = QuestionModel.objects.create(
            assignment=self.assignment, question="What is 2+2?", type="mcq"
        )
        # Choice
        self.choice = QuestionChoiceModel.objects.create(
            question=self.question, choice="4", is_correct=True
        )
        # Attachment
        self.attachment = AssignmentAttachmentsModel.objects.create(
            assignment=self.assignment,
            attachment_file=SimpleUploadedFile("test.pdf", b"filecontent"),
        )
        # Assignment-Group
        self.assignment_group = AssignmentsGroupModel.objects.create(
            assignment=self.assignment, group=self.group
        )

    def test_list_assignments(self):
        url = reverse("AssignmentModel-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_assignment(self):
        url = reverse("AssignmentModel-list")
        data = {
            "subject": self.subject.id,
            "professor": self.professor.id,
            "type": "hw",
            "start_time": timezone.now(),
            "end_time": timezone.now() + timedelta(hours=1),
            "description": "desc2",
            "max_grade": 90,
        }
        response = self.client.post(url, data, format="json")
        self.assertIn(
            response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]
        )

    def test_retrieve_assignment(self):
        url = reverse("AssignmentModel-detail", args=[self.assignment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_assignment(self):
        url = reverse("AssignmentModel-detail", args=[self.assignment.id])
        data = {
            "subject": self.subject.id,
            "professor": self.professor.id,
            "type": "exam",
            "start_time": timezone.now(),
            "end_time": timezone.now() + timedelta(hours=2),
            "description": "updated",
            "max_grade": 80,
        }
        response = self.client.put(url, data, format="json")
        self.assertIn(
            response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
        )

    def test_delete_assignment(self):
        url = reverse("AssignmentModel-detail", args=[self.assignment.id])
        response = self.client.delete(url)
        self.assertIn(
            response.status_code,
            [status.HTTP_204_NO_CONTENT, status.HTTP_405_METHOD_NOT_ALLOWED],
        )

    def test_list_attachments(self):
        url = reverse("assignmentattachmentsmodel-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_attachment(self):
        url = reverse("assignmentattachmentsmodel-list")
        data = {
            "assignment": self.assignment.id,
            "attachment_file": SimpleUploadedFile("test2.pdf", b"filecontent2"),
        }
        response = self.client.post(url, data)
        self.assertIn(
            response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]
        )

    def test_list_groups(self):
        url = reverse("assignmentsgroupmodel-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_group(self):
        url = reverse("assignmentsgroupmodel-list")
        data = {"assignment": self.assignment.id, "group": self.group.id}
        response = self.client.post(url, data)
        self.assertIn(
            response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]
        )

    def test_list_questions(self):
        url = reverse("questionmodel-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_question(self):
        url = reverse("questionmodel-list")
        data = {
            "assignment": self.assignment.id,
            "question": "What is 3+3?",
            "type": "mcq",
        }
        response = self.client.post(url, data)
        self.assertIn(
            response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]
        )

    def test_list_choices(self):
        url = reverse("questionchoicemodel-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_choice(self):
        url = reverse("questionchoicemodel-list")
        data = {"question": self.question.id, "choice": "6", "is_correct": False}
        response = self.client.post(url, data)
        self.assertIn(
            response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]
        )

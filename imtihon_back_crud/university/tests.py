from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from university.models import UniversityModel, FacultyModel, DepartmentModel, GroupModel, SubjectModel

class UniversityAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.university = UniversityModel.objects.create(user=self.user, name='Uni', location='Loc', longtitude='0', latitude='0', number='123', email='a@a.com', website='http://a.com', description='desc')
        self.faculty = FacultyModel.objects.create(university=self.university, name='Faculty', description='desc')
        self.department = DepartmentModel.objects.create(faculty=self.faculty, name='Dept', description='desc')
        self.group = GroupModel.objects.create(university=self.university, department=self.department, number=1)
        self.subject = SubjectModel.objects.create(university=self.university, department=self.department, name='Subj', description='desc')

    def test_list_universities(self):
        url = reverse('universitymodel-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_faculties(self):
        url = reverse('facultymodel-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_departments(self):
        url = reverse('departmentmodel-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_groups(self):
        url = reverse('groupmodel-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_subjects(self):
        url = reverse('subjectmodel-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

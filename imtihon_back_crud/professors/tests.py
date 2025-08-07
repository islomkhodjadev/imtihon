from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from professors.models import ProfessorProfileModel, ProfessorsSubjectModel
from university.models import UniversityModel, SubjectModel, FacultyModel, DepartmentModel

class ProfessorsAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.university = UniversityModel.objects.create(user=self.user, name='Uni', location='Loc', longtitude='0', latitude='0', number='123', email='a@a.com', website='http://a.com', description='desc')
        self.faculty = FacultyModel.objects.create(university=self.university, name='Faculty', description='desc')
        self.department = DepartmentModel.objects.create(faculty=self.faculty, name='Dept', description='desc')
        self.professor = ProfessorProfileModel.objects.create(user=self.user, university=self.university, professor_id='P001')
        self.subject = SubjectModel.objects.create(university=self.university, department=self.department, name='Subj', description='desc')
        self.prof_subject = ProfessorsSubjectModel.objects.create(professor=self.professor, subject=self.subject)

    def test_list_profiles(self):
        url = reverse('professorprofilemodel-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_subjects(self):
        url = reverse('professorssubjectmodel-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

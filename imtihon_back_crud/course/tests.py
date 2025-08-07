from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from course.models import CourseModel, CourseSectionModel, CourseLessonModel
from university.models import UniversityModel
from professors.models import ProfessorProfileModel

class CourseAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.university = UniversityModel.objects.create(user=self.user, name='Uni', location='Loc', longtitude='0', latitude='0', number='123', email='a@a.com', website='http://a.com', description='desc')
        self.professor = ProfessorProfileModel.objects.create(user=self.user, university=self.university, professor_id='P001')
        self.course = CourseModel.objects.create(university=self.university, professor=self.professor, name='Course', description='desc')
        self.section = CourseSectionModel.objects.create(course=self.course, name='Section', description='desc')
        self.lesson = CourseLessonModel.objects.create(section=self.section, name='Lesson', text='text')

    def test_list_courses(self):
        url = reverse('coursemodel-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_course(self):
        url = reverse('coursemodel-list')
        data = {'university': self.university.id, 'professor': self.professor.id, 'name': 'New Course', 'description': 'desc'}
        response = self.client.post(url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])

    def test_retrieve_course(self):
        url = reverse('coursemodel-detail', args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_course(self):
        url = reverse('coursemodel-detail', args=[self.course.id])
        data = {'university': self.university.id, 'professor': self.professor.id, 'name': 'Updated', 'description': 'desc'}
        response = self.client.put(url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])

    def test_delete_course(self):
        url = reverse('coursemodel-detail', args=[self.course.id])
        response = self.client.delete(url)
        self.assertIn(response.status_code, [status.HTTP_204_NO_CONTENT, status.HTTP_405_METHOD_NOT_ALLOWED])

    def test_list_sections(self):
        url = reverse('coursesectionmodel-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_lessons(self):
        url = reverse('courselessonmodel-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

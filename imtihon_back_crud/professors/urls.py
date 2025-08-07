from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfessorProfileModelViewSet, ProfessorsSubjectModelViewSet

router = DefaultRouter()
router.register(r'profiles', ProfessorProfileModelViewSet)
router.register(r'subjects', ProfessorsSubjectModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

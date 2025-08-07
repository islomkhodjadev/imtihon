from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UniversityModelViewSet,
    FacultyModelViewSet,
    DepartmentModelViewSet,
    GroupModelViewSet,
    SubjectModelViewSet,
    UniversityUrlsViewset,
)

router = DefaultRouter()
router.register(r"universities", UniversityModelViewSet)
router.register(r"faculties", FacultyModelViewSet)
router.register(r"departments", DepartmentModelViewSet)
router.register(r"groups", GroupModelViewSet)
router.register(r"subjects", SubjectModelViewSet)
router.register(r"university-urls", UniversityUrlsViewset)
urlpatterns = [
    path("", include(router.urls)),
]

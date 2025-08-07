from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseModelViewSet,
    CourseSectionModelViewSet,
    CourseLessonModelViewSet,
    CourseAttachmentModelViewSet,
    StudentCourseViewSet,
)

router = DefaultRouter()
router.register(r"courses", CourseModelViewSet)
router.register(r"sections", CourseSectionModelViewSet)
router.register(r"lessons", CourseLessonModelViewSet)
router.register(r"attachments", CourseAttachmentModelViewSet)
router.register(r"studentCourse", StudentCourseViewSet)
urlpatterns = [
    path("", include(router.urls)),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AssignmentModelViewSet,
    AssignmentAttachmentsModelViewSet,
    AssignmentsGroupModelViewSet,
    QuestionModelViewSet,
    QuestionChoiceModelViewSet,
)

router = DefaultRouter()
router.register(r"assignment", AssignmentModelViewSet)
router.register(r"attachments", AssignmentAttachmentsModelViewSet)
router.register(r"groups", AssignmentsGroupModelViewSet)
router.register(r"questions", QuestionModelViewSet)
router.register(r"choices", QuestionChoiceModelViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

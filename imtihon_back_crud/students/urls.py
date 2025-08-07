from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, CheatingEvidenceView

router = DefaultRouter()
router.register(r"", StudentViewSet, basename="student")

router.register(r"evidence", CheatingEvidenceView, basename="evidence")

urlpatterns = router.urls

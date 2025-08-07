from rest_framework.permissions import BasePermission, SAFE_METHODS
from university.models import UniversityModel
from students.models import StudentProfileModel
from professors.models import ProfessorProfileModel


class IsUniversityOwnerOrReadOnly(BasePermission):
    """
    Allows access only to university owners for unsafe methods, read-only for others.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # University owner
        if hasattr(obj, "user"):
            return obj.user == request.user
        # For related objects (faculty, department, etc.)
        if hasattr(obj, "university"):
            return getattr(obj.university, "user", None) == request.user
        return False


class IsProfessorOrReadOnly(BasePermission):
    """
    Custom permission: Only professors can create/update/delete, others can only read.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        # Only allow if user is a professor
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, "professor_profile")
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # Only allow professors to modify their own assignments
        if hasattr(request.user, "professor_profile"):
            return obj.professor == request.user.professor_profile
        return False


class IsProfessorsGroupAssignmentOrReadOnly(BasePermission):
    """
    Custom permission: Only professors can create/update/delete, others can only read.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        # Only allow if user is a professor
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, "professor_profile")
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # Only allow professors to modify their own assignments
        if hasattr(request.user, "professor_profile"):
            return obj.assignment.professor == request.user.professor_profile
        return False


class IsStudentOwnerOrReadOnly(BasePermission):
    """
    Allows access only to the student for unsafe methods, read-only for others.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # Student profile
        if hasattr(obj, "user"):
            return obj.user == request.user
        # For related objects (answers, sessions, etc.)
        if hasattr(obj, "student_profile"):
            return getattr(obj.student_profile, "user", None) == request.user
        return False


# permissions.py

from rest_framework.permissions import BasePermission
from accounts.models import APIKey
from django.utils.timezone import now

INTERNAL_HOSTS = {"127.0.0.1", "localhost", "fastapi_ai"}


class HasValidAPIKey(BasePermission):
    def has_permission(self, request, view):
        host = request.get_host().split(":")[0]  # Strip port if present
        if host in INTERNAL_HOSTS:
            return True

        key = request.headers.get("X-API-KEY")
        if not key:
            return False

        try:
            api_key = APIKey.objects.get(key=key, is_active=True)
            api_key.last_used_at = now()
            api_key.save(update_fields=["last_used_at"])
            return True
        except APIKey.DoesNotExist:
            return False

from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from professors.models import ProfessorProfileModel, ProfessorsSubjectModel
from .serializers import (
    ProfessorProfileModelSerializer,
    ProfessorsSubjectModelSerializer,
)
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsProfessorOwnerOrReadOnly


class ProfessorProfileModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing professor profiles in the educational system.

    This endpoint provides comprehensive professor profile management functionality, allowing
    administrators to create and manage professor information, academic credentials, and
    teaching assignments within the educational system.

    **Key Features:**
    - Create and manage professor profiles with professional information
    - Professor academic credentials and teaching history management
    - Integration with university structure and subject assignments
    - Support for professor-specific educational activities and course management
    - Professor profile metadata and administrative information management
    """

    queryset = ProfessorProfileModel.objects.all()
    permission_classes = [IsAuthenticated, IsProfessorOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return self.queryset.none()
        if hasattr(user, "professor_profile"):
            return ProfessorProfileModel.objects.filter(user=user)
        elif hasattr(user, "university"):
            return ProfessorProfileModel.objects.filter(university__user=user)
        return ProfessorProfileModel.objects.none()

    serializer_class = ProfessorProfileModelSerializer

    @swagger_auto_schema(
        tags=["Professor Profiles"],
        operation_summary="List all professor profiles",
        operation_description="Retrieve a comprehensive list of all professor profiles in the system with their professional information, academic credentials, and teaching assignments.",
        responses={
            200: openapi.Response(
                description="List of professor profiles retrieved successfully",
                schema=ProfessorProfileModelSerializer(many=True),
            ),
            401: "Unauthorized - Authentication required",
            403: "Forbidden - Insufficient permissions",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Professor Profiles"],
        operation_summary="Create a new professor profile",
        operation_description="Create a new professor profile with specified professional information, academic credentials, and teaching details.",
        request_body=ProfessorProfileModelSerializer,
        responses={
            201: openapi.Response(
                description="Professor profile created successfully",
                schema=ProfessorProfileModelSerializer,
            ),
            400: "Bad Request - Invalid data provided",
            401: "Unauthorized - Authentication required",
            403: "Forbidden - Insufficient permissions",
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Professor Profiles"],
        operation_summary="Retrieve a specific professor profile",
        operation_description="Get detailed information about a specific professor including their professional details, academic credentials, and teaching assignments.",
        responses={
            200: openapi.Response(
                description="Professor profile details retrieved successfully",
                schema=ProfessorProfileModelSerializer,
            ),
            404: "Not Found - Professor profile not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Professor Profiles"],
        operation_summary="Update a professor profile",
        operation_description="Update an existing professor's profile information including professional details, academic credentials, and teaching assignments.",
        request_body=ProfessorProfileModelSerializer,
        responses={
            200: openapi.Response(
                description="Professor profile updated successfully",
                schema=ProfessorProfileModelSerializer,
            ),
            400: "Bad Request - Invalid data provided",
            404: "Not Found - Professor profile not found",
            401: "Unauthorized - Authentication required",
            403: "Forbidden - Insufficient permissions",
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Professor Profiles"],
        operation_summary="Partially update a professor profile",
        operation_description="Update specific fields of an existing professor profile, such as professional details, academic credentials, or teaching assignments.",
        request_body=ProfessorProfileModelSerializer,
        responses={
            200: openapi.Response(
                description="Professor profile partially updated successfully",
                schema=ProfessorProfileModelSerializer,
            ),
            400: "Bad Request - Invalid data provided",
            404: "Not Found - Professor profile not found",
            401: "Unauthorized - Authentication required",
            403: "Forbidden - Insufficient permissions",
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Professor Profiles"],
        operation_summary="Delete a professor profile",
        operation_description="Permanently delete a professor profile from the system. This action will also remove all associated teaching assignments and subject associations.",
        responses={
            204: "No Content - Professor profile deleted successfully",
            404: "Not Found - Professor profile not found",
            401: "Unauthorized - Authentication required",
            403: "Forbidden - Insufficient permissions",
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ProfessorsSubjectModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing professor-subject associations.

    This endpoint handles the relationship between professors and the subjects they teach.
    It allows administrators to assign specific subjects to professors and manage teaching assignments.

    **Key Features:**
    - Associate professors with specific academic subjects
    - Manage professor teaching assignments and subject responsibilities
    - Track subject-specific teaching activities and course management
    - Support for professor-subject based educational programs and assessments
    - Teaching assignment metadata and administrative tracking
    """

    queryset = ProfessorsSubjectModel.objects.all()
    permission_classes = [IsAuthenticated, IsProfessorOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return self.queryset.none()
        if hasattr(user, "professor_profile"):
            return ProfessorsSubjectModel.objects.filter(professor__user=user)
        elif hasattr(user, "university"):
            return ProfessorsSubjectModel.objects.filter(
                professor__university__user=user
            )
        return ProfessorsSubjectModel.objects.none()

    serializer_class = ProfessorsSubjectModelSerializer

    @swagger_auto_schema(
        tags=["Professor Subjects"],
        operation_summary="List all professor-subject associations",
        operation_description="Retrieve all associations between professors and the subjects they teach with teaching assignment details.",
        responses={
            200: openapi.Response(
                description="List of professor-subject associations retrieved successfully",
                schema=ProfessorsSubjectModelSerializer(many=True),
            ),
            401: "Unauthorized - Authentication required",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Professor Subjects"],
        operation_summary="Create professor-subject association",
        operation_description="Associate a professor with a specific academic subject for teaching assignments and course management.",
        request_body=ProfessorsSubjectModelSerializer,
        responses={
            201: openapi.Response(
                description="Professor-subject association created successfully",
                schema=ProfessorsSubjectModelSerializer,
            ),
            400: "Bad Request - Invalid data provided",
            401: "Unauthorized - Authentication required",
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Professor Subjects"],
        operation_summary="Retrieve a specific professor-subject association",
        operation_description="Get detailed information about a specific professor-subject association including teaching assignment details.",
        responses={
            200: openapi.Response(
                description="Professor-subject association details retrieved successfully",
                schema=ProfessorsSubjectModelSerializer,
            ),
            404: "Not Found - Professor-subject association not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Professor Subjects"],
        operation_summary="Update professor-subject association",
        operation_description="Update an existing professor-subject association with modified teaching assignment details.",
        request_body=ProfessorsSubjectModelSerializer,
        responses={
            200: openapi.Response(
                description="Professor-subject association updated successfully",
                schema=ProfessorsSubjectModelSerializer,
            ),
            400: "Bad Request - Invalid data provided",
            404: "Not Found - Professor-subject association not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Professor Subjects"],
        operation_summary="Partially update professor-subject association",
        operation_description="Update specific fields of an existing professor-subject association, such as teaching assignment details.",
        request_body=ProfessorsSubjectModelSerializer,
        responses={
            200: openapi.Response(
                description="Professor-subject association partially updated successfully",
                schema=ProfessorsSubjectModelSerializer,
            ),
            400: "Bad Request - Invalid data provided",
            404: "Not Found - Professor-subject association not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Professor Subjects"],
        operation_summary="Delete professor-subject association",
        operation_description="Remove a professor-subject association, ending the teaching assignment for that subject.",
        responses={
            204: "No Content - Professor-subject association deleted successfully",
            404: "Not Found - Professor-subject association not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

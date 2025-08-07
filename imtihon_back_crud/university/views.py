from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from university.models import (
    UniversityModel,
    FacultyModel,
    DepartmentModel,
    GroupModel,
    SubjectModel,
)
from professors.models import ProfessorProfileModel
from accounts.models import UniversityUrlsModel
from accounts.serializers import UniversityUrlListSerializer
from .serializers import (
    UniversityModelSerializer,
    FacultyModelSerializer,
    DepartmentModelSerializer,
    GroupModelSerializer,
    SubjectModelSerializer,
)
from professors.serializers import ProfessorProfileModelSerializer
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsUniversityOwnerOrReadOnly

from rest_framework_simplejwt.authentication import JWTAuthentication


class UniversityModelViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "put", "patch", "head", "options"]

    """
    ViewSet for managing universities in the educational system.

    This endpoint provides comprehensive university management functionality, allowing
    administrators to create and manage educational institutions within the system.
    Universities serve as the top-level organizational structure for all educational activities.

    **Key Features:**
    - Create and manage university institutions
    - University metadata and information management
    - Integration with faculty and department structures
    - Support for multi-university educational systems
    - University-specific configuration and settings
    """

    authentication_classes = [JWTAuthentication]

    permission_classes = [IsAuthenticated, IsUniversityOwnerOrReadOnly]
    queryset = UniversityModel.objects.all()
    serializer_class = UniversityModelSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return UniversityModel.objects.none()
        if user.is_superuser:
            return UniversityModel.objects.all()
        if hasattr(user, "professor_profile"):
            return UniversityModel.objects.filter(id=user.professor_profile.university_id)
        if hasattr(user, "universities"):
            return UniversityModel.objects.filter(user=user)
        return UniversityModel.objects.none()

    @swagger_auto_schema(
        tags=["Universities"],
        operation_summary="List all universities",
        operation_description="Retrieve a comprehensive list of all universities in the system with their organizational details and structure.",
        responses={
            200: openapi.Response(
                description="List of universities retrieved successfully",
                schema=UniversityModelSerializer(many=True),
            ),
            401: "Unauthorized - Authentication required",
            403: "Forbidden - Insufficient permissions",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # @swagger_auto_schema(
    #     tags=["Universities"],
    #     operation_summary="Create a new university",
    #     operation_description="Create a new university institution with specified organizational structure and educational configuration.",
    #     request_body=UniversityModelSerializer,
    #     responses={
    #         201: openapi.Response(
    #             description="University created successfully",
    #             schema=UniversityModelSerializer,
    #         ),
    #         400: "Bad Request - Invalid data provided",
    #         401: "Unauthorized - Authentication required",
    #         403: "Forbidden - Insufficient permissions",
    #     },
    # )
    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Universities"],
        operation_summary="Retrieve a specific university",
        operation_description="Get detailed information about a specific university including its faculties, departments, and organizational structure.",
        responses={
            200: openapi.Response(
                description="University details retrieved successfully",
                schema=UniversityModelSerializer,
            ),
            404: "Not Found - University not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Universities"],
        operation_summary="Update a university",
        operation_description="Update an existing university's organizational structure, configuration, and institutional details.",
        request_body=UniversityModelSerializer,
        responses={
            200: openapi.Response(
                description="University updated successfully",
                schema=UniversityModelSerializer,
            ),
            400: "Bad Request - Invalid data provided",
            404: "Not Found - University not found",
            401: "Unauthorized - Authentication required",
            403: "Forbidden - Insufficient permissions",
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Universities"],
        operation_summary="Partially update a university",
        operation_description="Update specific fields of an existing university's organizational structure, configuration, and institutional details.",
        request_body=UniversityModelSerializer,
        responses={
            200: openapi.Response(
                description="University partially updated successfully",
                schema=UniversityModelSerializer,
            ),
            400: "Bad Request - Invalid data provided",
            404: "Not Found - University not found",
            401: "Unauthorized - Authentication required",
            403: "Forbidden - Insufficient permissions",
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # @swagger_auto_schema(
    #     tags=["Universities"],
    #     operation_summary="Delete a university",
    #     operation_description="Permanently delete a university from the system. This action will also remove all associated faculties, departments, and groups.",
    #     responses={
    #         204: "No Content - University deleted successfully",
    #         404: "Not Found - University not found",
    #         401: "Unauthorized - Authentication required",
    #         403: "Forbidden - Insufficient permissions",
    #     },
    # )
    # def destroy(self, request, *args, **kwargs):
    #     return super().destroy(request, *args, **kwargs)


class FacultyModelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for managing faculties within universities.

    This endpoint handles faculty management within university structures. Faculties
    represent major academic divisions within universities and contain multiple departments.

    **Key Features:**
    - Create and manage faculties within universities
    - Faculty-specific academic organization and structure
    - Integration with university and department hierarchies
    - Support for faculty-specific educational programs and policies
    - Faculty metadata and administrative information management
    """

    authentication_classes = [JWTAuthentication]

    permission_classes = [IsAuthenticated, IsUniversityOwnerOrReadOnly]
    queryset = FacultyModel.objects.all()
    serializer_class = FacultyModelSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return FacultyModel.objects.none()
        if user.is_superuser:
            return FacultyModel.objects.all()
        if hasattr(user, "professor_profile"):
            university = user.professor_profile.university
            return FacultyModel.objects.filter(university=university)
        if hasattr(user, "universities"):
            return FacultyModel.objects.filter(university__user=user)
        return FacultyModel.objects.none()

    @swagger_auto_schema(
        tags=["Universities"],
        operation_summary="List all faculties",
        operation_description="Retrieve all faculties across all universities with their organizational details and department structures.",
        responses={
            200: openapi.Response(
                description="List of faculties retrieved successfully",
                schema=FacultyModelSerializer(many=True),
            ),
            401: "Unauthorized - Authentication required",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # @swagger_auto_schema(
    #     tags=["Faculties"],
    #     operation_summary="Create a new faculty",
    #     operation_description="Create a new faculty within a university to organize academic departments and programs.",
    #     request_body=FacultyModelSerializer,
    #     responses={
    #         201: openapi.Response(
    #             description="Faculty created successfully",
    #             schema=FacultyModelSerializer,
    #         ),
    #         400: "Bad Request - Invalid data provided",
    #         401: "Unauthorized - Authentication required",
    #     },
    # )
    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Universities"],
        operation_summary="Retrieve a specific faculty",
        operation_description="Get detailed information about a specific faculty including its departments and organizational structure.",
        responses={
            200: openapi.Response(
                description="Faculty details retrieved successfully",
                schema=FacultyModelSerializer,
            ),
            404: "Not Found - Faculty not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # @swagger_auto_schema(
    #     tags=["Universities"],
    #     operation_summary="Update a faculty",
    #     operation_description="Update an existing faculty's organizational structure and academic details.",
    #     request_body=FacultyModelSerializer,
    #     responses={
    #         200: openapi.Response(
    #             description="Faculty updated successfully",
    #             schema=FacultyModelSerializer,
    #         ),
    #         400: "Bad Request - Invalid data provided",
    #         404: "Not Found - Faculty not found",
    #         401: "Unauthorized - Authentication required",
    #     },
    # )
    # def update(self, request, *args, **kwargs):
    #     return super().update(request, *args, **kwargs)

    # @swagger_auto_schema(
    #     tags=["Universities"],
    #     operation_summary="Partially update a faculty",
    #     operation_description="Update specific fields of an existing faculty's organizational structure and academic details.",
    #     request_body=FacultyModelSerializer,
    #     responses={
    #         200: openapi.Response(
    #             description="Faculty partially updated successfully",
    #             schema=FacultyModelSerializer,
    #         ),
    #         400: "Bad Request - Invalid data provided",
    #         404: "Not Found - Faculty not found",
    #         401: "Unauthorized - Authentication required",
    #     },
    # )
    # def partial_update(self, request, *args, **kwargs):
    #     return super().partial_update(request, *args, **kwargs)

    # @swagger_auto_schema(
    #     tags=["Universities"],
    #     operation_summary="Delete a faculty",
    #     operation_description="Permanently delete a faculty from the system. This action will also remove all associated departments and groups.",
    #     responses={
    #         204: "No Content - Faculty deleted successfully",
    #         404: "Not Found - Faculty not found",
    #         401: "Unauthorized - Authentication required",
    #     },
    # )
    # def destroy(self, request, *args, **kwargs):
    #     return super().destroy(request, *args, **kwargs)


class DepartmentModelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for managing departments within faculties.

    This endpoint handles department management within faculty structures. Departments
    represent specialized academic units that focus on specific fields of study.

    **Key Features:**
    - Create and manage departments within faculties
    - Department-specific academic programs and curriculum
    - Integration with faculty and group hierarchies
    - Support for department-specific subjects and courses
    - Department metadata and academic information management
    """

    permission_classes = [IsAuthenticated, IsUniversityOwnerOrReadOnly]
    queryset = DepartmentModel.objects.all()
    serializer_class = DepartmentModelSerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return DepartmentModel.objects.none()
        if user.is_superuser:
            return DepartmentModel.objects.all()
        if hasattr(user, "professor_profile"):
            university = user.professor_profile.university
            return DepartmentModel.objects.filter(faculty__university=university)
        if hasattr(user, "universities"):
            return DepartmentModel.objects.filter(faculty__university__user=user)
        return DepartmentModel.objects.none()

    @swagger_auto_schema(
        tags=["Universities"],
        operation_summary="List all departments",
        operation_description="Retrieve all departments across all faculties with their academic programs and organizational details.",
        responses={
            200: openapi.Response(
                description="List of departments retrieved successfully",
                schema=DepartmentModelSerializer(many=True),
            ),
            401: "Unauthorized - Authentication required",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # @swagger_auto_schema(
    #     tags=["Universities"],
    #     operation_summary="Create a new department",
    #     operation_description="Create a new department within a faculty to organize specialized academic programs and subjects.",
    #     request_body=DepartmentModelSerializer,
    #     responses={
    #         201: openapi.Response(
    #             description="Department created successfully",
    #             schema=DepartmentModelSerializer,
    #         ),
    #         400: "Bad Request - Invalid data provided",
    #         401: "Unauthorized - Authentication required",
    #     },
    # )
    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Universities"],
        operation_summary="Retrieve a specific department",
        operation_description="Get detailed information about a specific department including its groups and academic programs.",
        responses={
            200: openapi.Response(
                description="Department details retrieved successfully",
                schema=DepartmentModelSerializer,
            ),
            404: "Not Found - Department not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # @swagger_auto_schema(
    #     tags=["Universities"],
    #     operation_summary="Update a department",
    #     operation_description="Update an existing department's academic programs and organizational details.",
    #     request_body=DepartmentModelSerializer,
    #     responses={
    #         200: openapi.Response(
    #             description="Department updated successfully",
    #             schema=DepartmentModelSerializer,
    #         ),
    #         400: "Bad Request - Invalid data provided",
    #         404: "Not Found - Department not found",
    #         401: "Unauthorized - Authentication required",
    #     },
    # )
    # def update(self, request, *args, **kwargs):
    #     return super().update(request, *args, **kwargs)

    # @swagger_auto_schema(
    #     tags=["Universities"],
    #     operation_summary="Partially update a department",
    #     operation_description="Update specific fields of an existing department's academic programs and organizational details.",
    #     request_body=DepartmentModelSerializer,
    #     responses={
    #         200: openapi.Response(
    #             description="Department partially updated successfully",
    #             schema=DepartmentModelSerializer,
    #         ),
    #         400: "Bad Request - Invalid data provided",
    #         404: "Not Found - Department not found",
    #         401: "Unauthorized - Authentication required",
    #     },
    # )
    # def partial_update(self, request, *args, **kwargs):
    #     return super().partial_update(request, *args, **kwargs)

    # @swagger_auto_schema(
    #     tags=["Universities"],
    #     operation_summary="Delete a department",
    #     operation_description="Permanently delete a department from the system. This action will also remove all associated groups and subjects.",
    #     responses={
    #         204: "No Content - Department deleted successfully",
    #         404: "Not Found - Department not found",
    #         401: "Unauthorized - Authentication required",
    #     },
    # )
    # def destroy(self, request, *args, **kwargs):
    #     return super().destroy(request, *args, **kwargs)


class GroupModelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for managing student groups within departments.

    This endpoint handles student group management within department structures. Groups
    represent cohorts of students who study together and share common academic schedules.

    **Key Features:**
    - Create and manage student groups within departments
    - Group-specific academic schedules and assignments
    - Integration with department and subject hierarchies
    - Support for group-based learning and assessment
    - Group metadata and student cohort information management
    """

    permission_classes = [IsAuthenticated, IsUniversityOwnerOrReadOnly]
    queryset = GroupModel.objects.all()
    serializer_class = GroupModelSerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return GroupModel.objects.none()
        if user.is_superuser:
            return GroupModel.objects.all()
        if hasattr(user, "professor_profile"):
            university = user.professor_profile.university
            return GroupModel.objects.filter(university=university)
        if hasattr(user, "universities"):
            return GroupModel.objects.filter(university__user=user)
        return GroupModel.objects.none()

    @swagger_auto_schema(
        tags=["Universities"],
        operation_summary="List all student groups",
        operation_description="Retrieve all student groups across all departments with their academic schedules and cohort information.",
        responses={
            200: openapi.Response(
                description="List of student groups retrieved successfully",
                schema=GroupModelSerializer(many=True),
            ),
            401: "Unauthorized - Authentication required",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # @swagger_auto_schema(
    #     tags=["Student Groups"],
    #     operation_summary="Create a new student group",
    #     operation_description="Create a new student group within a department to organize student cohorts and academic schedules.",
    #     request_body=GroupModelSerializer,
    #     responses={
    #         201: openapi.Response(
    #             description="Student group created successfully",
    #             schema=GroupModelSerializer,
    #         ),
    #         400: "Bad Request - Invalid data provided",
    #         401: "Unauthorized - Authentication required",
    #     },
    # )
    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Universities"],
        operation_summary="Retrieve a specific student group",
        operation_description="Get detailed information about a specific student group including its academic schedule and cohort details.",
        responses={
            200: openapi.Response(
                description="Student group details retrieved successfully",
                schema=GroupModelSerializer,
            ),
            404: "Not Found - Student group not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # @swagger_auto_schema(
    #     tags=["Student Groups"],
    #     operation_summary="Update a student group",
    #     operation_description="Update an existing student group's academic schedule and cohort details.",
    #     request_body=GroupModelSerializer,
    #     responses={
    #         200: openapi.Response(
    #             description="Student group updated successfully",
    #             schema=GroupModelSerializer,
    #         ),
    #         400: "Bad Request - Invalid data provided",
    #         404: "Not Found - Student group not found",
    #         401: "Unauthorized - Authentication required",
    #     },
    # )
    # def update(self, request, *args, **kwargs):
    #     return super().update(request, *args, **kwargs)

    # @swagger_auto_schema(
    #     tags=["Student Groups"],
    #     operation_summary="Partially update a student group",
    #     operation_description="Update specific fields of an existing student group's academic schedule and cohort details.",
    #     request_body=GroupModelSerializer,
    #     responses={
    #         200: openapi.Response(
    #             description="Student group partially updated successfully",
    #             schema=GroupModelSerializer,
    #         ),
    #         400: "Bad Request - Invalid data provided",
    #         404: "Not Found - Student group not found",
    #         401: "Unauthorized - Authentication required",
    #     },
    # )
    # def partial_update(self, request, *args, **kwargs):
    #     return super().partial_update(request, *args, **kwargs)

    # @swagger_auto_schema(
    #     tags=["Student Groups"],
    #     operation_summary="Delete a student group",
    #     operation_description="Permanently delete a student group from the system. This action will also remove all associated student enrollments.",
    #     responses={
    #         204: "No Content - Student group deleted successfully",
    #         404: "Not Found - Student group not found",
    #         401: "Unauthorized - Authentication required",
    #     },
    # )
    # def destroy(self, request, *args, **kwargs):
    #     return super().destroy(request, *args, **kwargs)


class SubjectModelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for managing subjects within the educational system.

    This endpoint handles subject management across the educational system. Subjects
    represent specific academic disciplines or courses that are taught to students.

    **Key Features:**
    - Create and manage academic subjects
    - Subject-specific curriculum and learning objectives
    - Integration with department and assignment hierarchies
    - Support for subject-based course and assignment management
    - Subject metadata and academic information management
    """

    permission_classes = [IsAuthenticated, IsUniversityOwnerOrReadOnly]
    queryset = SubjectModel.objects.all()
    serializer_class = SubjectModelSerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return SubjectModel.objects.none()
        if user.is_superuser:
            return SubjectModel.objects.all()
        if hasattr(user, "professor_profile"):
            university = user.professor_profile.university
            return SubjectModel.objects.filter(university=university)
        if hasattr(user, "universities"):
            return SubjectModel.objects.filter(university__user=user)
        return SubjectModel.objects.none()

    @swagger_auto_schema(
        tags=["Universities"],
        operation_summary="List all subjects",
        operation_description="Retrieve all academic subjects in the system with their curriculum details and educational information.",
        responses={
            200: openapi.Response(
                description="List of subjects retrieved successfully",
                schema=SubjectModelSerializer(many=True),
            ),
            401: "Unauthorized - Authentication required",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # @swagger_auto_schema(
    #     tags=["Subjects"],
    #     operation_summary="Create a new subject",
    #     operation_description="Create a new academic subject with specified curriculum, learning objectives, and educational requirements.",
    #     request_body=SubjectModelSerializer,
    #     responses={
    #         201: openapi.Response(
    #             description="Subject created successfully",
    #             schema=SubjectModelSerializer,
    #         ),
    #         400: "Bad Request - Invalid data provided",
    #         401: "Unauthorized - Authentication required",
    #     },
    # )
    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Universities"],
        operation_summary="Retrieve a specific subject",
        operation_description="Get detailed information about a specific academic subject including its curriculum and learning objectives.",
        responses={
            200: openapi.Response(
                description="Subject details retrieved successfully",
                schema=SubjectModelSerializer,
            ),
            404: "Not Found - Subject not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # @swagger_auto_schema(
    #     tags=["Subjects"],
    #     operation_summary="Update a subject",
    #     operation_description="Update an existing subject's curriculum, learning objectives, and educational requirements.",
    #     request_body=SubjectModelSerializer,
    #     responses={
    #         200: openapi.Response(
    #             description="Subject updated successfully",
    #             schema=SubjectModelSerializer,
    #         ),
    #         400: "Bad Request - Invalid data provided",
    #         404: "Not Found - Subject not found",
    #         401: "Unauthorized - Authentication required",
    #     },
    # )
    # def update(self, request, *args, **kwargs):
    #     return super().update(request, *args, **kwargs)

    # @swagger_auto_schema(
    #     tags=["Subjects"],
    #     operation_summary="Partially update a subject",
    #     operation_description="Update specific fields of an existing subject's curriculum, learning objectives, and educational requirements.",
    #     request_body=SubjectModelSerializer,
    #     responses={
    #         200: openapi.Response(
    #             description="Subject partially updated successfully",
    #             schema=SubjectModelSerializer,
    #         ),
    #         400: "Bad Request - Invalid data provided",
    #         404: "Not Found - Subject not found",
    #         401: "Unauthorized - Authentication required",
    #     },
    # )
    # def partial_update(self, request, *args, **kwargs):
    #     return super().partial_update(request, *args, **kwargs)

    # @swagger_auto_schema(
    #     tags=["Subjects"],
    #     operation_summary="Delete a subject",
    #     operation_description="Permanently delete a subject from the system. This action will also remove all associated assignments and courses.",
    #     responses={
    #         204: "No Content - Subject deleted successfully",
    #         404: "Not Found - Subject not found",
    #         401: "Unauthorized - Authentication required",
    #     },
    # )
    # def destroy(self, request, *args, **kwargs):
    #     return super().destroy(request, *args, **kwargs)


class ProfessorProfileReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for managing professor profiles within universities.

    This endpoint handles professor profile management within university structures.
    Professors represent academic staff members who teach and conduct research.

    **Key Features:**
    - Create and manage professor profiles within universities
    - Professor-specific academic qualifications and experience
    - Integration with university and department hierarchies
    - Support for professor-specific educational programs and policies
    - Professor metadata and administrative information management
    """

    permission_classes = [IsAuthenticated, IsUniversityOwnerOrReadOnly]
    queryset = ProfessorProfileModel.objects.all()
    serializer_class = ProfessorProfileModelSerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return ProfessorProfileModel.objects.none()
        if user.is_superuser:
            return ProfessorProfileModel.objects.all()
        if hasattr(user, "professor_profile"):
            university = user.professor_profile.university
            return ProfessorProfileModel.objects.filter(university=university)
        if hasattr(user, "universities"):
            return ProfessorProfileModel.objects.filter(university__user=user)
        return ProfessorProfileModel.objects.none()

    @swagger_auto_schema(
        tags=["Universities"],
        operation_summary="List all professor profiles",
        operation_description="Retrieve all professor profiles across all universities with their academic qualifications and experience.",
        responses={
            200: openapi.Response(
                description="List of professor profiles retrieved successfully",
                schema=ProfessorProfileModelSerializer(many=True),
            ),
            401: "Unauthorized - Authentication required",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # @swagger_auto_schema(
    #     tags=["Universities"],
    #     operation_summary="Create a new professor profile",
    #     operation_description="Create a new professor profile within a university to organize academic qualifications and experience.",
    #     request_body=ProfessorProfileModelSerializer,
    #     responses={
    #         201: openapi.Response(
    #             description="Professor profile created successfully",
    #             schema=ProfessorProfileModelSerializer,
    #         ),
    #         400: "Bad Request - Invalid data provided",
    #         401: "Unauthorized - Authentication required",
    #     },
    # )
    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Universities"],
        operation_summary="Retrieve a specific professor profile",
        operation_description="Get detailed information about a specific professor profile including their academic qualifications and experience.",
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

    # @swagger_auto_schema(
    #     tags=["Professors"],
    #     operation_summary="Update a professor profile",
    #     operation_description="Update an existing professor profile's academic qualifications and experience.",
    #     request_body=ProfessorProfileModelSerializer,
    #     responses={
    #         200: openapi.Response(
    #             description="Professor profile updated successfully",
    #             schema=ProfessorProfileModelSerializer,
    #         ),
    #         400: "Bad Request - Invalid data provided",
    #         404: "Not Found - Professor profile not found",
    #         401: "Unauthorized - Authentication required",
    #     },
    # )
    # def update(self, request, *args, **kwargs):
    #     return super().update(request, *args, **kwargs)

    # @swagger_auto_schema(
    #     tags=["Professors"],
    #     operation_summary="Partially update a professor profile",
    #     operation_description="Update specific fields of an existing professor profile's academic qualifications and experience.",
    #     request_body=ProfessorProfileModelSerializer,
    #     responses={
    #         200: openapi.Response(
    #             description="Professor profile partially updated successfully",
    #             schema=ProfessorProfileModelSerializer,
    #         ),
    #         400: "Bad Request - Invalid data provided",
    #         404: "Not Found - Professor profile not found",
    #         401: "Unauthorized - Authentication required",
    #     },
    # )
    # def partial_update(self, request, *args, **kwargs):
    #     return super().partial_update(request, *args, **kwargs)

    # @swagger_auto_schema(
    #     tags=["Professors"],
    #     operation_summary="Delete a professor profile",
    #     operation_description="Permanently delete a professor profile from the system. This action will also remove all associated academic qualifications and experience.",
    #     responses={
    #         204: "No Content - Professor profile deleted successfully",
    #         404: "Not Found - Professor profile not found",
    #         401: "Unauthorized - Authentication required",
    #     },
    # )
    # def destroy(self, request, *args, **kwargs):
    #     return super().destroy(request, *args, **kwargs)


class UniversityUrlsViewset(viewsets.ReadOnlyModelViewSet):
    queryset = UniversityUrlsModel.objects.all()
    serializer_class = UniversityUrlListSerializer

    @swagger_auto_schema(
        tags=["Universities"],
        operation_summary="List all university urls for login code",
        operation_description="Retrieve all university urls with codes.",
        responses={
            200: openapi.Response(
                description="List of University urls retrieved successfully",
                schema=ProfessorProfileModelSerializer(many=True),
            ),
            401: "Bad request",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Universities"],
        operation_summary="Retrieve a specific university url",
        operation_description="Get detailed information about a specific university url.",
        responses={
            200: openapi.Response(
                description="University url details retrieved successfully",
                schema=ProfessorProfileModelSerializer,
            ),
            404: "Not Found - University url not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

from django.shortcuts import render
from rest_framework import viewsets, response, status, serializers
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import (
    CourseModel,
    CourseSectionModel,
    CourseLessonModel,
    CourseAttachmentsModel,
)
from students.models import StudentCourseModel
from students.serializers import StudentCourseProgressModelSerializer
from .serializers import (
    CourseModelSerializer,
    CourseSectionModelSerializer,
    CourseLessonModelSerializer,
    CourseAttachmentModelSerializer,  # fix import
)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from students.serializers import (
    StudentCourseModelSerializer,
    StudentCourseProgressModel,
)

# Create your views here.


class CourseModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing courses in the educational system.

    This endpoint provides comprehensive course management functionality, allowing
    administrators and professors to create, organize, and manage educational courses.
    Courses serve as the primary containers for educational content and are organized
    into sections and lessons.

    **Key Features:**
    - Create and manage complete courses
    - Organize courses with structured content hierarchy
    - Support for various course formats and delivery methods
    - Course metadata management including descriptions and requirements
    - Integration with university structure and subject assignments
    """

    queryset = CourseModel.objects.all()
    serializer_class = CourseModelSerializer
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return CourseModel.objects.none()

        if hasattr(self.request.user, "student_profile"):
            return CourseModel.objects.filter(
                subject__university=self.request.user.student_profile.university
            )

        if hasattr(self.request.user, "professor_profile"):
            return CourseModel.objects.filter(
                subject__university=self.request.user.professor_profile.university
            )
        if hasattr(self.request.user, "university"):
            return CourseModel.objects.filter(
                subject__university=self.request.user.university
            )

    @swagger_auto_schema(
        tags=["Courses"],
        operation_summary="List all courses",
        operation_description="Retrieve a comprehensive list of all courses in the system with their details, structure, and metadata.",
        responses={
            200: openapi.Response(
                description="List of courses retrieved successfully",
                schema=CourseModelSerializer(many=True),
            ),
            401: "Unauthorized - Authentication required",
            403: "Forbidden - Insufficient permissions",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Courses"],
        operation_summary="Create a new course",
        operation_description="Create a new course with specified structure, content organization, and educational requirements.",
        request_body=CourseModelSerializer,
        responses={
            201: openapi.Response(
                description="Course created successfully", schema=CourseModelSerializer
            ),
            400: "Bad Request - Invalid data provided",
            401: "Unauthorized - Authentication required",
            403: "Forbidden - Insufficient permissions",
        },
    )
    def create(self, request, *args, **kwargs):
        user = request.user

        if hasattr(user, "student_profile"):
            return response.Response(
                data={"detail": "Students are not allowed to create courses."},
                status=status.HTTP_403_FORBIDDEN,
            )
        if not (hasattr(user, "professor_profile") or hasattr(user, "university")):
            return response.Response(
                {"detail": "Only professors or university staff can create courses."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Courses"],
        operation_summary="Retrieve a specific course",
        operation_description="Get detailed information about a specific course including its structure, sections, and lessons.",
        responses={
            200: openapi.Response(
                description="Course details retrieved successfully",
                schema=CourseModelSerializer,
            ),
            404: "Not Found - Course not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Courses"],
        operation_summary="Update a course",
        operation_description="Update an existing course's structure, content organization, and educational requirements.",
        request_body=CourseModelSerializer,
        responses={
            200: openapi.Response(
                description="Course updated successfully", schema=CourseModelSerializer
            ),
            400: "Bad Request - Invalid data provided",
            404: "Not Found - Course not found",
            401: "Unauthorized - Authentication required",
            403: "Forbidden - Insufficient permissions",
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Courses"],
        operation_summary="Partially update a course",
        operation_description="Update specific fields of an existing course.",
        request_body=CourseModelSerializer,
        responses={
            200: openapi.Response(
                description="Course partially updated successfully",
                schema=CourseModelSerializer,
            ),
            400: "Bad Request - Invalid data provided",
            404: "Not Found - Course not found",
            401: "Unauthorized - Authentication required",
            403: "Forbidden - Insufficient permissions",
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Courses"],
        operation_summary="Delete a course",
        operation_description="Permanently delete a course from the system. This action will also remove all associated sections and lessons.",
        responses={
            204: "No Content - Course deleted successfully",
            404: "Not Found - Course not found",
            401: "Unauthorized - Authentication required",
            403: "Forbidden - Insufficient permissions",
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CourseSectionModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing course sections.

    This endpoint handles the organization of courses into logical sections or modules.
    Sections provide a hierarchical structure within courses, allowing for better
    content organization and learning progression.

    **Key Features:**
    - Create and manage course sections/modules
    - Organize course content into logical units
    - Support for section-specific metadata and descriptions
    - Enable structured learning progression within courses
    - Integration with course hierarchy and lesson management
    """

    queryset = CourseSectionModel.objects.all()
    serializer_class = CourseSectionModelSerializer
    parser_classes = (MultiPartParser, FormParser)

    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return CourseSectionModel.objects.none()

        if hasattr(self.request.user, "student_profile"):
            return CourseSectionModel.objects.filter(
                course__subject__university=self.request.user.student_profile.university
            )

        if hasattr(self.request.user, "professor_profile"):
            return CourseSectionModel.objects.filter(
                course__subject__university=self.request.user.professor_profile.university
            )
        if hasattr(self.request.user, "university"):
            return CourseSectionModel.objects.filter(
                course__subject__university=self.request.user.university
            )

    @swagger_auto_schema(
        tags=["Course Sections"],
        operation_summary="List all course sections",
        operation_description="Retrieve all course sections with their organizational structure and content details.",
        responses={
            200: openapi.Response(
                description="List of course sections retrieved successfully",
                schema=CourseSectionModelSerializer(many=True),
            ),
            401: "Unauthorized - Authentication required",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        methods=["get"],
        operation_summary="Get sections by course id",
        manual_parameters=[
            openapi.Parameter(
                "course_id",
                openapi.IN_QUERY,
                description="ID of the course",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        responses={200: CourseSectionModelSerializer},
        tags=["Course Sections"],
    )
    @action(detail=False, methods=["get"], url_path="course-sections")
    def get_course_sectionss(self, request):
        course_id = request.query_params.get("course_id")
        if not course_id:
            raise serializers.ValidationError(
                "Missing 'course_id' in query parameters."
            )

        user = request.user

        if hasattr(user, "student_profile"):
            university = user.student_profile.university

        elif hasattr(user, "professor_profile"):
            university = user.professor_profile.university
        elif hasattr(user, "university"):
            university = user.university

        else:
            return response.Response(
                {"detail": "User is not associated with a university."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = CourseSectionModel.objects.filter(
            course__id=course_id, course__subject__university=university
        )

        return response.Response(
            data=CourseSectionModelSerializer(data, many=True).data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        tags=["Course Sections"],
        operation_summary="Create a new course section",
        operation_description="Create a new section within a course to organize content into logical learning units.",
        request_body=CourseSectionModelSerializer,
        responses={
            201: openapi.Response(
                description="Course section created successfully",
                schema=CourseSectionModelSerializer,
            ),
            400: "Bad Request - Invalid data provided",
            401: "Unauthorized - Authentication required",
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Course Sections"],
        operation_summary="Retrieve a specific course section",
        operation_description="Get detailed information about a specific course section by its ID.",
        responses={
            200: openapi.Response(
                description="Course section details retrieved successfully",
                schema=CourseSectionModelSerializer,
            ),
            404: "Not Found - Course section not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Course Sections"],
        operation_summary="Update a course section",
        operation_description="Update an existing course section's details.",
        request_body=CourseSectionModelSerializer,
        responses={
            200: openapi.Response(
                description="Course section updated successfully",
                schema=CourseSectionModelSerializer,
            ),
            400: "Bad Request - Invalid data provided",
            404: "Not Found - Course section not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Course Sections"],
        operation_summary="Partially update a course section",
        operation_description="Update specific fields of an existing course section.",
        request_body=CourseSectionModelSerializer,
        responses={
            200: openapi.Response(
                description="Course section partially updated successfully",
                schema=CourseSectionModelSerializer,
            ),
            400: "Bad Request - Invalid data provided",
            404: "Not Found - Course section not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Course Sections"],
        operation_summary="Delete a course section",
        operation_description="Permanently delete a course section from the system.",
        responses={
            204: "No Content - Course section deleted successfully",
            404: "Not Found - Course section not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CourseLessonModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing course lessons.

    This endpoint handles individual lessons within course sections. Lessons are the
    smallest content units in the course hierarchy and contain the actual educational
    material that students will consume.

    **Key Features:**
    - Create and manage individual lessons within course sections
    - Support for various lesson content types and formats
    - Lesson-specific metadata and learning objectives
    - Integration with course and section hierarchy
    - Enable detailed content organization and delivery
    """

    queryset = CourseLessonModel.objects.all()
    serializer_class = CourseLessonModelSerializer
    parser_classes = (MultiPartParser, FormParser)

    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return CourseLessonModel.objects.none()

        if hasattr(self.request.user, "student_profile"):
            return CourseLessonModel.objects.filter(
                section__course__subject__university=self.request.user.student_profile.university
            )

        if hasattr(self.request.user, "professor_profile"):
            return CourseLessonModel.objects.filter(
                section__course__subject__university=self.request.user.professor_profile.university
            )

        if hasattr(self.request.user, "university"):
            return CourseLessonModel.objects.filter(
                section__course__subject__university=self.request.user.university
            )

    @swagger_auto_schema(
        tags=["Course Lessons"],
        operation_summary="List all course lessons",
        operation_description="Retrieve all lessons across all courses and sections with their content details.",
        responses={
            200: openapi.Response(
                description="List of course lessons retrieved successfully",
                schema=CourseLessonModelSerializer(many=True),
            ),
            401: "Unauthorized - Authentication required",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Course Lessons"],
        operation_summary="Create a new course lesson",
        operation_description="Create a new lesson within a course section containing educational content and learning materials.",
        request_body=CourseLessonModelSerializer,
        responses={
            201: openapi.Response(
                description="Course lesson created successfully",
                schema=CourseLessonModelSerializer,
            ),
            400: "Bad Request - Invalid data provided",
            401: "Unauthorized - Authentication required",
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Course Lessons"],
        operation_summary="Retrieve a specific course lesson",
        operation_description="Get detailed information about a specific course lesson by its ID.",
        responses={
            200: openapi.Response(
                description="Course lesson details retrieved successfully",
                schema=CourseLessonModelSerializer,
            ),
            404: "Not Found - Course lesson not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Course Lessons"],
        operation_summary="Update a course lesson",
        operation_description="Update an existing course lesson's details.",
        request_body=CourseLessonModelSerializer,
        responses={
            200: openapi.Response(
                description="Course lesson updated successfully",
                schema=CourseLessonModelSerializer,
            ),
            400: "Bad Request - Invalid data provided",
            404: "Not Found - Course lesson not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Course Lessons"],
        operation_summary="Partially update a course lesson",
        operation_description="Update specific fields of an existing course lesson.",
        request_body=CourseLessonModelSerializer,
        responses={
            200: openapi.Response(
                description="Course lesson partially updated successfully",
                schema=CourseLessonModelSerializer,
            ),
            400: "Bad Request - Invalid data provided",
            404: "Not Found - Course lesson not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Course Lessons"],
        operation_summary="Delete a course lesson",
        operation_description="Permanently delete a course lesson from the system.",
        responses={
            204: "No Content - Course lesson deleted successfully",
            404: "Not Found - Course lesson not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CourseAttachmentModelViewSet(viewsets.ModelViewSet):
    queryset = CourseAttachmentsModel.objects.all()
    serializer_class = CourseAttachmentModelSerializer
    parser_classes = (MultiPartParser, FormParser)

    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return CourseAttachmentsModel.objects.none()

        if hasattr(self.request.user, "student_profile"):
            return CourseAttachmentsModel.objects.filter(
                course__subject__university=self.request.user.student_profile.university
            )

        if hasattr(self.request.user, "professor_profile"):
            return CourseModel.objects.filter(
                course__subject__university=self.request.user.professor_profile.university
            )
        if hasattr(self.request.user, "university"):
            return CourseAttachmentsModel.objects.filter(
                course__subject__university=self.request.user.university
            )

    @swagger_auto_schema(
        tags=["Course Attachments"],
        operation_summary="List all course attachments",
        operation_description="Retrieve a list of all file attachments associated with courses.",
        responses={
            200: openapi.Response(
                description="List of attachments retrieved successfully",
                schema=CourseAttachmentModelSerializer(many=True),
            ),
            401: "Unauthorized - Authentication required",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Course Attachments"],
        operation_summary="Upload a new attachment",
        operation_description="Upload a new file attachment for a course. Supports various file formats.",
        request_body=CourseAttachmentModelSerializer,
        responses={
            201: openapi.Response(
                description="Attachment uploaded successfully",
                schema=CourseAttachmentModelSerializer,
            ),
            400: "Bad Request - Invalid file or data provided",
            401: "Unauthorized - Authentication required",
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Course Attachments"],
        operation_summary="Retrieve a specific attachment",
        operation_description="Get detailed information about a specific course attachment by its ID.",
        responses={
            200: openapi.Response(
                description="Attachment details retrieved successfully",
                schema=CourseAttachmentModelSerializer,
            ),
            404: "Not Found - Attachment not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Course Attachments"],
        operation_summary="Update a course attachment",
        operation_description="Update an existing course attachment's details.",
        request_body=CourseAttachmentModelSerializer,
        responses={
            200: openapi.Response(
                description="Attachment updated successfully",
                schema=CourseAttachmentModelSerializer,
            ),
            400: "Bad Request - Invalid data provided",
            404: "Not Found - Attachment not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Course Attachments"],
        operation_summary="Partially update a course attachment",
        operation_description="Update specific fields of an existing course attachment.",
        request_body=CourseAttachmentModelSerializer,
        responses={
            200: openapi.Response(
                description="Attachment partially updated successfully",
                schema=CourseAttachmentModelSerializer,
            ),
            400: "Bad Request - Invalid data provided",
            404: "Not Found - Attachment not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Course Attachments"],
        operation_summary="Delete a course attachment",
        operation_description="Permanently delete a course attachment from the system.",
        responses={
            204: "No Content - Attachment deleted successfully",
            404: "Not Found - Attachment not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class StudentCourseViewSet(viewsets.ViewSet):
    queryset = StudentCourseModel.objects.all()
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        methods=["post"],
        operation_summary="Start Learning Course",
        request_body=StudentCourseModelSerializer,
        responses={200: StudentCourseModelSerializer()},
        tags=["Student"],
    )
    @action(methods=["post"], detail=False, url_path="student-course-start")
    def student_course(self, request):
        data = request.data

        if not hasattr(request.user, "student_profile"):
            return response.Response({"detail": "Not a student."}, status=404)
        student = request.user.student_profile

        serializer = StudentCourseModelSerializer(
            data=data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)
        instance = serializer.save(student=student, start_time=timezone.now())
        return response.Response(
            data=StudentCourseModelSerializer(instance=instance).data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        methods=["patch"],
        operation_summary="End Learning Course",
        request_body=StudentCourseModelSerializer,
        responses={200: StudentCourseModelSerializer()},
        tags=["Student"],
    )
    @action(methods=["patch"], detail=False, url_path="student-course-end")
    def student_course_end(self, request):
        data = request.data

        if not hasattr(request.user, "student_profile"):
            return response.Response({"detail": "Not a student."}, status=404)
        student = request.user.student_profile
        course_id = request.data.get("course")
        if not course_id:
            return response.Response({"detail": "Course ID is required."}, status=400)
        try:
            instance = StudentCourseModel.objects.get(
                student=student, course_id=course_id
            )
            if instance.end_time:
                raise serializers.ValidationError("this course already ended")
        except StudentCourseModel.DoesNotExist:
            return response.Response({"detail": "Enrollment not found."}, status=404)

        serializer = StudentCourseModelSerializer(
            instance, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        instance = serializer.save(end_time=timezone.now(), is_completed=True)

        return response.Response(
            StudentCourseModelSerializer(instance).data, status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        methods=["post"],
        operation_summary="Add Learning progress",
        request_body=StudentCourseProgressModelSerializer,
        responses={200: StudentCourseProgressModelSerializer()},
        tags=["Student"],
    )
    @action(methods=["post"], detail=False, url_path="add-progress")
    def add_progress(self, request):
        if not hasattr(request.user, "student_profile"):
            return response.Response({"detail": "Not a student."}, status=404)

        serialized_data = StudentCourseProgressModelSerializer(
            data=request.data, context={"request": request}
        )

        serialized_data.is_valid(raise_exception=True)

        instance = serialized_data.save()

        return response.Response(
            data=StudentCourseProgressModelSerializer(instance).data,
            status=status.HTTP_201_CREATED,
        )

    @swagger_auto_schema(
        methods=["post"],
        operation_summary="Complete lesson progress",
        tags=["Student"],
    )
    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        if not hasattr(request.user, "student_profile"):
            return response.Response({"detail": "Not a student."}, status=404)

        student = request.user.student_profile

        try:
            progress = StudentCourseProgressModel.objects.get(
                pk=pk, student_course__student=student
            )
        except StudentCourseProgressModel.DoesNotExist:
            return response.Response({"detail": "Progress not found."}, status=404)

        if progress.is_completed:
            return response.Response(
                {"detail": "Lesson is already completed."}, status=200
            )

        progress.is_completed = True
        progress.save()

        return response.Response({"detail": "Lesson marked as completed."}, status=200)

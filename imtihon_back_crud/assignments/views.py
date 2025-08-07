from django.shortcuts import render
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from assignments.models import (
    AssignmentModel,
    AssignmentAttachmentsModel,
    AssignmentsGroupModel,
    QuestionModel,
    QuestionChoiceModel,
)
from .serializers import (
    AssignmentModelSerializer,
    AssignmentAttachmentsModelSerializer,
    AssignmentsGroupModelSerializer,
    QuestionModelSerializer,
    QuestionChoiceModelSerializer,
    AssignmentCreateSerializer,
)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from core.permissions import (
    IsProfessorOrReadOnly,
    IsProfessorsGroupAssignmentOrReadOnly,
)
from rest_framework import serializers
from .serializers import QuestionCreateSerializer

# Create your views here.


class AssignmentModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing assignments in the educational system.

    This endpoint provides CRUD operations for assignments, which are the core assessment
    components in the educational system. Assignments can be of different types including
    homework, exams, projects, and quizzes.

    **Assignment Types:**
    - `hw`: Homework assignments
    - `exam`: Examination assignments
    - `project`: Project-based assignments
    - `quiz`: Quiz assignments

    **Key Features:**
    - Create, read, update, and delete assignments
    - Assign assignments to specific subjects and professors
    - Set time constraints with start and end times
    - Define maximum grades for assessment
    - Include detailed descriptions for student guidance
    """

    queryset = AssignmentModel.objects.all()
    serializer_class = AssignmentModelSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsProfessorOrReadOnly]

    def get_serializer_class(self):
        if self.action == "create":
            return AssignmentCreateSerializer
        return AssignmentModelSerializer

    def perform_create(self, serializer):
        user = self.request.user
        professor = getattr(user, "professor_profile", None)
        if not professor:
            raise serializers.ValidationError("Only professors can create assignments.")
        subject_id = self.request.data.get("subject")
        if not subject_id:
            raise serializers.ValidationError("Subject is required.")
        from university.models import SubjectModel
        from professors.models import ProfessorsSubjectModel

        try:
            subject = SubjectModel.objects.get(id=subject_id)
        except SubjectModel.DoesNotExist:
            raise serializers.ValidationError("Subject not found.")
        # Check that this subject is assigned to this professor
        if not ProfessorsSubjectModel.objects.filter(
            professor=professor, subject=subject
        ).exists():
            raise serializers.ValidationError(
                "You can only assign subjects that are assigned to you as a professor."
            )
        serializer.save(professor=professor, subject=subject)

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return AssignmentModel.objects.none()
        # Professors see their own assignments
        if hasattr(user, "professor_profile"):
            return AssignmentModel.objects.filter(professor=user.professor_profile)
        # University owners see all assignments for their university
        if hasattr(user, "universities"):
            return AssignmentModel.objects.filter(professor__university__user=user)
        # Students see assignments for their university or group
        if hasattr(user, "student_profile"):
            student = user.student_profile
            return AssignmentModel.objects.filter(
                professor__university=student.university
            )
        return AssignmentModel.objects.none()

    @swagger_auto_schema(
        tags=["Assignments"],
        operation_summary="List all assignments",
        operation_description="Retrieve a list of all assignments in the system with their details including subject, professor, type, and time constraints.",
        responses={
            200: openapi.Response(
                description="List of assignments retrieved successfully",
                schema=AssignmentModelSerializer(many=True),
            ),
            401: "Unauthorized - Authentication required",
            403: "Forbidden - Insufficient permissions",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Assignments"],
        operation_summary="Create a new assignment",
        operation_description="Create a new assignment with specified subject, professor, type, time constraints, and description.",
        request_body=AssignmentCreateSerializer,
        responses={
            201: AssignmentCreateSerializer,
            400: "Bad Request - Invalid data provided",
            401: "Unauthorized - Authentication required",
            403: "Forbidden - Insufficient permissions",
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Assignments"],
        operation_summary="Retrieve a specific assignment",
        operation_description="Get detailed information about a specific assignment by its ID.",
        responses={
            200: openapi.Response(
                description="Assignment details retrieved successfully",
                schema=AssignmentModelSerializer,
            ),
            404: "Not Found - Assignment not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Assignments"],
        operation_summary="Update an assignment",
        operation_description="Update an existing assignment's details including subject, professor, type, time constraints, and description.",
        request_body=AssignmentModelSerializer,
        responses={
            200: openapi.Response(
                description="Assignment updated successfully",
                schema=AssignmentModelSerializer,
            ),
            400: "Bad Request - Invalid data provided",
            404: "Not Found - Assignment not found",
            401: "Unauthorized - Authentication required",
            403: "Forbidden - Insufficient permissions",
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Assignments"],
        operation_summary="Partially update an assignment",
        operation_description="Update specific fields of an existing assignment.",
        request_body=AssignmentModelSerializer,
        responses={
            200: openapi.Response(
                description="Assignment partially updated successfully",
                schema=AssignmentModelSerializer,
            ),
            400: "Bad Request - Invalid data provided",
            404: "Not Found - Assignment not found",
            401: "Unauthorized - Authentication required",
            403: "Forbidden - Insufficient permissions",
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Assignments"],
        operation_summary="Delete an assignment",
        operation_description="Permanently delete an assignment from the system. This action cannot be undone.",
        responses={
            204: "No Content - Assignment deleted successfully",
            404: "Not Found - Assignment not found",
            401: "Unauthorized - Authentication required",
            403: "Forbidden - Insufficient permissions",
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class AssignmentAttachmentsModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing assignment attachments.

    This endpoint handles file attachments associated with assignments. Attachments
    can include supplementary materials, reference documents, or any files that
    need to be provided to students along with the assignment.

    **Supported Features:**
    - Upload and manage files attached to assignments
    - Associate multiple files with a single assignment
    - Retrieve attachment information and download files
    - Delete attachments when no longer needed
    """

    queryset = AssignmentAttachmentsModel.objects.all()
    serializer_class = AssignmentAttachmentsModelSerializer
    parser_classes = (MultiPartParser, FormParser)

    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=["Assignment Attachments"],
        operation_summary="List all assignment attachments",
        operation_description="Retrieve a list of all file attachments associated with assignments.",
        responses={
            200: openapi.Response(
                description="List of attachments retrieved successfully",
                schema=AssignmentAttachmentsModelSerializer(many=True),
            ),
            401: "Unauthorized - Authentication required",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Assignment Attachments"],
        operation_summary="Upload a new attachment",
        operation_description="Upload a new file attachment for an assignment. Supports various file formats.",
        request_body=AssignmentAttachmentsModelSerializer,
        responses={
            201: openapi.Response(
                description="Attachment uploaded successfully",
                schema=AssignmentAttachmentsModelSerializer,
            ),
            400: "Bad Request - Invalid file or data provided",
            401: "Unauthorized - Authentication required",
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Assignment Attachments"],
        operation_summary="Retrieve a specific attachment",
        operation_description="Get detailed information about a specific assignment attachment by its ID.",
        responses={
            200: openapi.Response(
                description="Attachment details retrieved successfully",
                schema=AssignmentAttachmentsModelSerializer,
            ),
            404: "Not Found - Attachment not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Assignment Attachments"],
        operation_summary="Update an attachment",
        operation_description="Update an existing assignment attachment's details.",
        request_body=AssignmentAttachmentsModelSerializer,
        responses={
            200: openapi.Response(
                description="Attachment updated successfully",
                schema=AssignmentAttachmentsModelSerializer,
            ),
            400: "Bad Request - Invalid data provided",
            404: "Not Found - Attachment not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Assignment Attachments"],
        operation_summary="Partially update an attachment",
        operation_description="Update specific fields of an existing assignment attachment.",
        request_body=AssignmentAttachmentsModelSerializer,
        responses={
            200: openapi.Response(
                description="Attachment partially updated successfully",
                schema=AssignmentAttachmentsModelSerializer,
            ),
            400: "Bad Request - Invalid data provided",
            404: "Not Found - Attachment not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Assignment Attachments"],
        operation_summary="Delete an attachment",
        operation_description="Permanently delete an assignment attachment from the system.",
        responses={
            204: "No Content - Attachment deleted successfully",
            404: "Not Found - Attachment not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class AssignmentsGroupModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing assignment-group associations.

    This endpoint manages the relationship between assignments and student groups.
    It allows professors to assign specific assignments to particular groups of students,
    enabling targeted assessment and group-specific assignment management.

    **Key Features:**
    - Associate assignments with specific student groups
    - Manage group-specific assignment access
    - Control which groups can access which assignments
    - Enable targeted assessment strategies
    """

    queryset = AssignmentsGroupModel.objects.all()
    serializer_class = AssignmentsGroupModelSerializer
    permission_classes = [IsProfessorsGroupAssignmentOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return AssignmentsGroupModel.objects.none()
        if hasattr(user, "professor_profile"):
            return AssignmentsGroupModel.objects.filter(
                assignment__professor=user.professor_profile
            )
        if hasattr(user, "universities"):
            return AssignmentsGroupModel.objects.filter(
                assignment__professor__university__user=user
            )
        if hasattr(user, "student_profile"):
            return AssignmentsGroupModel.objects.filter(
                assignment__professor__university=user.student_profile.university
            )
        return AssignmentsGroupModel.objects.none()

    @swagger_auto_schema(
        tags=["Assignment Groups"],
        operation_summary="List all assignment-group associations",
        operation_description="Retrieve all associations between assignments and student groups.",
        responses={
            200: openapi.Response(
                description="List of assignment-group associations retrieved successfully",
                schema=AssignmentsGroupModelSerializer(many=True),
            ),
            401: "Unauthorized - Authentication required",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Assignment Groups"],
        operation_summary="Create assignment-group association",
        operation_description="Associate an assignment with a specific student group for targeted assessment.",
        request_body=AssignmentsGroupModelSerializer,
        responses={
            201: openapi.Response(
                description="Assignment-group association created successfully",
                schema=AssignmentsGroupModelSerializer,
            ),
            400: "Bad Request - Invalid data provided",
            401: "Unauthorized - Authentication required",
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Assignment Groups"],
        operation_summary="Retrieve a specific assignment-group association",
        operation_description="Get detailed information about a specific assignment-group association by its ID.",
        responses={
            200: openapi.Response(
                description="Assignment-group association details retrieved successfully",
                schema=AssignmentsGroupModelSerializer,
            ),
            404: "Not Found - Association not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Assignment Groups"],
        operation_summary="Update an assignment-group association",
        operation_description="Update an existing assignment-group association's details.",
        request_body=AssignmentsGroupModelSerializer,
        responses={
            200: openapi.Response(
                description="Assignment-group association updated successfully",
                schema=AssignmentsGroupModelSerializer,
            ),
            400: "Bad Request - Invalid data provided",
            404: "Not Found - Association not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Assignment Groups"],
        operation_summary="Partially update an assignment-group association",
        operation_description="Update specific fields of an existing assignment-group association.",
        request_body=AssignmentsGroupModelSerializer,
        responses={
            200: openapi.Response(
                description="Assignment-group association partially updated successfully",
                schema=AssignmentsGroupModelSerializer,
            ),
            400: "Bad Request - Invalid data provided",
            404: "Not Found - Association not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Assignment Groups"],
        operation_summary="Delete an assignment-group association",
        operation_description="Permanently delete an assignment-group association from the system.",
        responses={
            204: "No Content - Association deleted successfully",
            404: "Not Found - Association not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class QuestionModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing questions within assignments.

    This endpoint handles the creation and management of questions that are part of assignments.
    Questions can be of different types including multiple choice, open-ended, and true/false questions.

    **Question Types:**
    - `mcq`: Multiple choice questions with predefined answer options
    - `open`: Open-ended questions requiring text responses
    - `true_false`: True or false questions with boolean answers

    **Key Features:**
    - Create questions of various types for assignments
    - Manage question content and answer formats
    - Support for different assessment methodologies
    - Flexible question structure for diverse educational needs
    """

    queryset = QuestionModel.objects.all()
    serializer_class = QuestionModelSerializer
    permission_classes = [IsProfessorOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def get_serializer_class(self):
        if self.action == "create":
            return QuestionCreateSerializer
        return QuestionModelSerializer

    def perform_create(self, serializer):
        user = self.request.user
        professor = getattr(user, "professor_profile", None)
        # Assignment must be provided in the request data
        assignment_id = self.request.data.get("assignment")
        if not assignment_id:
            raise serializers.ValidationError("Assignment is required.")
        try:
            assignment = AssignmentModel.objects.get(
                id=assignment_id, professor=professor
            )
        except AssignmentModel.DoesNotExist:
            raise serializers.ValidationError(
                "Assignment not found or not owned by you."
            )
        serializer.save(assignment=assignment)

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return QuestionModel.objects.none()
        if hasattr(user, "professor_profile"):
            return QuestionModel.objects.filter(
                assignment__professor=user.professor_profile
            )
        if hasattr(user, "universities"):
            return QuestionModel.objects.filter(
                assignment__professor__university__user=user
            )
        if hasattr(user, "student_profile"):
            return QuestionModel.objects.filter(
                assignment__professor__university=user.student_profile.university
            )
        return QuestionModel.objects.none()

    @swagger_auto_schema(
        tags=["Questions"],
        operation_summary="List all questions",
        operation_description="Retrieve all questions from assignments, including their types and content.",
        responses={
            200: openapi.Response(
                description="List of questions retrieved successfully",
                schema=QuestionModelSerializer(many=True),
            ),
            401: "Unauthorized - Authentication required",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Questions"],
        operation_summary="Create a new question",
        operation_description="Create a new question for an assignment with specified type and content.",
        request_body=QuestionCreateSerializer,
        responses={
            201: QuestionCreateSerializer,
            400: "Bad Request - Invalid data provided",
            401: "Unauthorized - Authentication required",
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Questions"],
        operation_summary="Retrieve a specific question",
        operation_description="Get detailed information about a specific question by its ID.",
        responses={
            200: openapi.Response(
                description="Question details retrieved successfully",
                schema=QuestionModelSerializer,
            ),
            404: "Not Found - Question not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Questions"],
        operation_summary="Update a question",
        operation_description="Update an existing question's details.",
        request_body=QuestionModelSerializer,
        responses={
            200: openapi.Response(
                description="Question updated successfully",
                schema=QuestionModelSerializer,
            ),
            400: "Bad Request - Invalid data provided",
            404: "Not Found - Question not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Questions"],
        operation_summary="Partially update a question",
        operation_description="Update specific fields of an existing question.",
        request_body=QuestionModelSerializer,
        responses={
            200: openapi.Response(
                description="Question partially updated successfully",
                schema=QuestionModelSerializer,
            ),
            400: "Bad Request - Invalid data provided",
            404: "Not Found - Question not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Questions"],
        operation_summary="Delete a question",
        operation_description="Permanently delete a question from the system.",
        responses={
            204: "No Content - Question deleted successfully",
            404: "Not Found - Question not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class QuestionChoiceModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing multiple choice question options.

    This endpoint handles the answer choices for multiple choice questions (MCQ).
    It allows creation and management of answer options with correct/incorrect indicators.

    **Key Features:**
    - Create answer choices for multiple choice questions
    - Mark specific choices as correct or incorrect
    - Manage the complete set of options for each MCQ
    - Support for various MCQ formats and complexity levels
    """

    queryset = QuestionChoiceModel.objects.all()
    serializer_class = QuestionChoiceModelSerializer
    permission_classes = [IsProfessorOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return QuestionChoiceModel.objects.none()
        if hasattr(user, "professor_profile"):
            return QuestionChoiceModel.objects.filter(
                question__assignment__professor=user.professor_profile
            )
        if hasattr(user, "universities"):
            return QuestionChoiceModel.objects.filter(
                question__assignment__professor__university__user=user
            )
        if hasattr(user, "student_profile"):
            return QuestionChoiceModel.objects.filter(
                question__assignment__professor__university=user.student_profile.university
            )
        return QuestionChoiceModel.objects.none()

    @swagger_auto_schema(
        tags=["Question Choices"],
        operation_summary="List all question choices",
        operation_description="Retrieve all answer choices for multiple choice questions.",
        responses={
            200: openapi.Response(
                description="List of question choices retrieved successfully",
                schema=QuestionChoiceModelSerializer(many=True),
            ),
            401: "Unauthorized - Authentication required",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Question Choices"],
        operation_summary="Create a new question choice",
        operation_description="Create a new answer choice for a multiple choice question with correct/incorrect indicator.",
        request_body=QuestionChoiceModelSerializer,
        responses={
            201: openapi.Response(
                description="Question choice created successfully",
                schema=QuestionChoiceModelSerializer,
            ),
            400: "Bad Request - Invalid data provided",
            401: "Unauthorized - Authentication required",
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Question Choices"],
        operation_summary="Retrieve a specific question choice",
        operation_description="Get detailed information about a specific question choice by its ID.",
        responses={
            200: openapi.Response(
                description="Question choice details retrieved successfully",
                schema=QuestionChoiceModelSerializer,
            ),
            404: "Not Found - Question choice not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Question Choices"],
        operation_summary="Update a question choice",
        operation_description="Update an existing question choice's details.",
        request_body=QuestionChoiceModelSerializer,
        responses={
            200: openapi.Response(
                description="Question choice updated successfully",
                schema=QuestionChoiceModelSerializer,
            ),
            400: "Bad Request - Invalid data provided",
            404: "Not Found - Question choice not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Question Choices"],
        operation_summary="Partially update a question choice",
        operation_description="Update specific fields of an existing question choice.",
        request_body=QuestionChoiceModelSerializer,
        responses={
            200: openapi.Response(
                description="Question choice partially updated successfully",
                schema=QuestionChoiceModelSerializer,
            ),
            400: "Bad Request - Invalid data provided",
            404: "Not Found - Question choice not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Question Choices"],
        operation_summary="Delete a question choice",
        operation_description="Permanently delete a question choice from the system.",
        responses={
            204: "No Content - Question choice deleted successfully",
            404: "Not Found - Question choice not found",
            401: "Unauthorized - Authentication required",
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

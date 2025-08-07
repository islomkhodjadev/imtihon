from rest_framework import viewsets, response, status, views, parsers
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.permissions import HasValidAPIKey
from students.models import (
    StudentProfileModel,
    StudentCourseModel,
    StudentCourseProgressModel,
    StudentSessionModel,
    CheatingEvidenceModel,
    StudentAnswerModel,
    StudentTimetableModel,
)
from .serializers import (
    StudentProfileModelSerializer,
    StudentCourseModelSerializer,
    StudentCourseProgressModelSerializer,
    StudentSessionModelSerializer,
    CheatingEvidenceModelSerializer,
    StudentAnswerModelSerializer,
    StudentTimetableModelSerializer,
    StudentSessionStartModelSerializer,
)
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsStudentOwnerOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.utils import timezone
from django.db.models import Count


class StudentViewSet(viewsets.ViewSet):
    """
    Unified Student API: All student info and actions in one place.
    Only the authenticated student can access/manipulate their own data.
    """

    permission_classes = [IsAuthenticated, IsStudentOwnerOrReadOnly]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        methods=["get"],
        operation_summary="Get my student profile",
        responses={200: StudentProfileModelSerializer},
        tags=["Student"],
    )
    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        user = request.user
        if not user.is_authenticated:
            return response.Response({"detail": "Not a student."}, status=404)
        profile = getattr(user, "student_profile", None)
        if not profile:
            return response.Response({"detail": "Not a student."}, status=404)
        return response.Response(StudentProfileModelSerializer(profile).data)

    @swagger_auto_schema(
        methods=["put", "patch"],
        operation_summary="Update my student profile",
        request_body=StudentProfileModelSerializer,
        responses={200: StudentProfileModelSerializer},
        tags=["Student"],
    )
    @action(detail=False, methods=["put", "patch"], url_path="me")
    def update_me(self, request):
        user = request.user
        if not user.is_authenticated:
            return response.Response({"detail": "Not a student."}, status=404)
        profile = getattr(user, "student_profile", None)
        if not profile:
            return response.Response({"detail": "Not a student."}, status=404)
        serializer = StudentProfileModelSerializer(
            profile, data=request.data, partial=(request.method == "PATCH")
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)

    # @swagger_auto_schema(
    #     methods=['delete'],
    #     operation_summary="Delete my student profile",
    #     responses={204: "No Content"},
    #     tags=["Student"],
    # )
    # @action(detail=False, methods=["delete"], url_path="me")
    # def delete_me(self, request):
    #     user = request.user
    #     profile = getattr(user, "student_profile", None)
    #     if not profile:
    #         return response.Response({"detail": "Not a student."}, status=404)
    #     profile.delete()
    #     return response.Response(status=204)

    @swagger_auto_schema(
        methods=["get"],
        operation_summary="Get my timetable",
        responses={200: StudentTimetableModelSerializer(many=True)},
        tags=["Student"],
    )
    @action(detail=False, methods=["get"], url_path="timetable")
    def timetable(self, request):
        user = request.user
        if not user.is_authenticated:
            return response.Response({"detail": "Not a student."}, status=404)
        profile = getattr(user, "student_profile", None)
        if not profile:
            return response.Response({"detail": "Not a student."}, status=404)
        timetables = StudentTimetableModel.objects.filter(
            group__students__student=profile
        )
        return response.Response(
            StudentTimetableModelSerializer(timetables, many=True).data
        )

    @swagger_auto_schema(
        methods=["get"],
        operation_summary="Get my courses",
        responses={200: StudentCourseModelSerializer(many=True)},
        tags=["Student"],
    )
    @action(detail=False, methods=["get"], url_path="courses")
    def courses(self, request):
        user = request.user
        if not user.is_authenticated:
            return response.Response({"detail": "Not a student."}, status=404)
        profile = getattr(user, "student_profile", None)
        if not profile:
            return response.Response({"detail": "Not a student."}, status=404)
        courses = StudentCourseModel.objects.filter(student=profile)
        return response.Response(StudentCourseModelSerializer(courses, many=True).data)

    @swagger_auto_schema(
        methods=["get"],
        operation_summary="Get my course progress",
        responses={200: StudentCourseProgressModelSerializer(many=True)},
        tags=["Student"],
    )
    @action(detail=False, methods=["get"], url_path="progress")
    def progress(self, request):
        user = request.user
        if not user.is_authenticated:
            return response.Response({"detail": "Not a student."}, status=404)
        profile = getattr(user, "student_profile", None)
        if not profile:
            return response.Response({"detail": "Not a student."}, status=404)
        progress = StudentCourseProgressModel.objects.filter(
            student_course__student=profile
        )
        return response.Response(
            StudentCourseProgressModelSerializer(progress, many=True).data
        )

    @swagger_auto_schema(
        methods=["get"],
        operation_summary="Get my sessions",
        responses={200: StudentSessionModelSerializer(many=True)},
        tags=["Student"],
    )
    @action(detail=False, methods=["get"], url_path="sessions")
    def sessions(self, request):
        user = request.user
        if not user.is_authenticated:
            return response.Response({"detail": "Not a student."}, status=404)
        profile = getattr(user, "student_profile", None)
        if not profile:
            return response.Response({"detail": "Not a student."}, status=404)
        sessions = StudentSessionModel.objects.filter(student=profile)
        return response.Response(
            StudentSessionModelSerializer(sessions, many=True).data
        )

    @swagger_auto_schema(
        methods=["get"],
        operation_summary="Get my answers",
        responses={200: StudentAnswerModelSerializer(many=True)},
        tags=["Student"],
    )
    @action(detail=False, methods=["get"], url_path="answers")
    def answers(self, request):
        user = request.user
        if not user.is_authenticated:
            return response.Response({"detail": "Not a student."}, status=404)
        profile = getattr(user, "student_profile", None)
        if not profile:
            return response.Response({"detail": "Not a student."}, status=404)
        answers = StudentAnswerModel.objects.filter(session__student=profile)
        return response.Response(StudentAnswerModelSerializer(answers, many=True).data)

    @swagger_auto_schema(
        methods=["get"],
        operation_summary="Get my cheating evidence",
        responses={200: CheatingEvidenceModelSerializer(many=True)},
        tags=["Student"],
    )
    @action(detail=False, methods=["get"], url_path="cheating-evidence")
    def cheating_evidence(self, request):
        user = request.user
        if not user.is_authenticated:
            return response.Response({"detail": "Not a student."}, status=404)
        profile = getattr(user, "student_profile", None)
        if not profile:
            return response.Response({"detail": "Not a student."}, status=404)
        evidence = CheatingEvidenceModel.objects.filter(session__student=profile)
        return response.Response(
            CheatingEvidenceModelSerializer(evidence, many=True).data
        )

    @swagger_auto_schema(
        methods=["post"],
        operation_summary="Start Session",
        request_body=StudentSessionStartModelSerializer,
        responses={200: StudentSessionModelSerializer()},
        tags=["Student"],
    )
    @action(detail=False, methods=["post"], url_path="session-start")
    def session_start(self, request):
        user = request.user

        if not user.is_authenticated:
            return response.Response({"detail": "Not a student."}, status=404)
        profile = getattr(user, "student_profile", None)
        if not profile:
            return response.Response({"detail": "Not a student."}, status=404)

        if profile.sessions.filter(end_time=None).exists():
            return response.Response(
                {"detail": "You have session which was not ended."}, status=404
            )

        data = request.data
        data["student"] = profile
        print(data["student"])
        serialized_data = StudentSessionStartModelSerializer(data=data)

        if serialized_data.is_valid(raise_exception=True):
            instance = serialized_data.save(student=profile)
            return response.Response(
                data=StudentSessionModelSerializer(instance=instance).data,
                status=status.HTTP_200_OK,
            )

        return response.Response(
            serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
        )

    @swagger_auto_schema(
        methods=["patch"],
        operation_summary="End Session",
        request_body=type(
            "StudentSessionInputSerializer",
            (serializers.Serializer,),
            {
                "session_id": serializers.IntegerField(),
            },
        ),
        responses={200: StudentSessionModelSerializer()},
        tags=["Student"],
    )
    @action(detail=False, methods=["patch"], url_path="session-end")
    def session_end(self, request):
        user = request.user

        if not user.is_authenticated:
            return response.Response({"detail": "Not a student."}, status=404)
        profile = getattr(user, "student_profile", None)
        if not profile:
            return response.Response({"detail": "Not a student."}, status=404)

        if not profile.sessions.filter(end_time=None).exists():
            return response.Response(
                {"detail": "You have no session to end."}, status=404
            )
        session_id = request.data.get("session_id")
        if session_id is None:
            return response.Response({"detail": "Session id not provided"}, status=404)

        session = profile.sessions.filter(id=session_id)
        if not session.exists():
            return response.Response(
                {"detail": f"You have no session with id: {session_id} ."}, status=404
            )
        session = session.first()
        session.end_time = timezone.now()

        counts = session.cheating_evidence.values("type").annotate(count=Count("id"))
        count_map = {item["type"]: item["count"] for item in counts}

        # Step 2: Normalize each metric (1 = evidence present, 0 = clean)
        metrics = {
            "device": 1 if count_map.get("device", 0) > 0 else 0,
            "multiple_people": 1 if count_map.get("multiple_people", 0) > 0 else 0,
            "audio": 1 if count_map.get("audio", 0) > 0 else 0,
            "ai": 1 if count_map.get("ai", 0) > 0 else 0,
        }

        # Normalize tab_switch (scale from 0 to 1, max = 5)
        raw_tab_switch = count_map.get("tab_switch", 0)
        ts_norm = min(raw_tab_switch / 5.0, 1.0)
        metrics["tab_switch"] = ts_norm

        # Step 3: Weights (equal weight for each of 5 types)
        weights = {
            "device": 0.20,
            "multiple_people": 0.20,
            "audio": 0.20,
            "ai": 0.20,
            "tab_switch": 0.20,
        }

        # Step 4: Compute raw score (0–1)
        raw_score = sum(weights[key] * (1 - metrics[key]) for key in weights)

        # Step 5: Convert to percentage
        score_percent = int(round(raw_score * 100))

        session.cheating_score = 100 - score_percent
        session.save()

        return response.Response(
            data=StudentSessionModelSerializer(session).data, status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        methods=["post"],
        operation_summary="Submit an answer to a question",
        request_body=StudentAnswerModelSerializer,
        responses={200: StudentAnswerModelSerializer()},
        tags=["Student"],
    )
    @action(detail=False, methods=["post"], url_path="answer-question")
    def answer_question(self, request):
        user = request.user

        # Ensure the user is authenticated and is a student
        if not user.is_authenticated:
            return response.Response({"detail": "Authentication required."}, status=401)

        profile = getattr(user, "student_profile", None)
        if not profile:
            return response.Response({"detail": "Not a student."}, status=403)

        # Validate and save answer
        serialized_data = StudentAnswerModelSerializer(
            data=request.data, context={"request": request}
        )

        if serialized_data.is_valid(raise_exception=True):
            instance = serialized_data.save()
            return response.Response(
                data=StudentAnswerModelSerializer(instance).data,
                status=status.HTTP_200_OK,
            )

        return response.Response(
            serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
        )


class CheatingEvidenceView(viewsets.ViewSet):

    permission_classes = [HasValidAPIKey]
    parser_classes = [parsers.MultiPartParser, parsers.JSONParser]

    @swagger_auto_schema(
        operation_summary="Submit Cheating evidence",
        request_body=CheatingEvidenceModelSerializer,
        responses={200: CheatingEvidenceModelSerializer()},
        tags=["Services"],
    )
    def create(self, request):
        data = request.data
        serializer = CheatingEvidenceModelSerializer(data=data)

        serializer.is_valid(raise_exception=True)
        evidence = serializer.save()

        return response.Response(
            data=CheatingEvidenceModelSerializer(evidence).data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        operation_summary="Submit liveness of student",
        request_body=type(
            "IsLiveSerializer",
            (serializers.Serializer,),
            {
                "is_live": serializers.BooleanField(),
                "session_id": serializers.IntegerField(),
            },
        ),
        responses={200: StudentSessionModelSerializer()},
        tags=["Services"],
    )
    @action(detail=False, methods=["post"], url_path="live-check")
    def live_check(self, request):

        data = request.data
        session_id = data.get("session_id")
        is_live = data.get("is_live")
        if session_id is None or is_live is None:
            return response.Response(
                {"status": "you must pass exactly session_id and is_live"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        session = StudentSessionModel.objects.filter(
            id=session_id, end_time__isnull=True
        ).first()

        if not session:
            return response.Response(
                {"status": "session_id doesnt exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        session.is_live = True
        session.save()
        return response.Response(
            data=StudentSessionModelSerializer(instance=session).data,
            status=status.HTTP_200_OK,
        )

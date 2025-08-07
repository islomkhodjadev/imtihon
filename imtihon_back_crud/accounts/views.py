from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    UniversityRegistrationSerializer,
    StudentRegistrationSerializer,
    ProfessorRegistrationSerializer,
    LoginSerializer,
    ExternalLoginSerializer,  # new
)
from drf_yasg.utils import swagger_auto_schema
from accounts.models import UniversityUrlsModel
from rest_framework.permissions import IsAdminUser
from students.models import (
    StudentProfileModel,
    StudentSubjectModel,
    StudentTimetableModel,
    StudentTimeTablesubjectModel,
)
from professors.models import ProfessorProfileModel, ProfessorsSubjectModel
from accounts.models import UniversityUrlsModel
import requests
from university.models import (
    FacultyModel,
    DepartmentModel,
    GroupModel,
    UniversityModel,
    SubjectModel,
)
from django.contrib.auth import get_user_model
import datetime
from django.db import transaction

# Create your views here.


class UniversityRegistrationView(generics.CreateAPIView):
    serializer_class = UniversityRegistrationSerializer

    @swagger_auto_schema(tags=["Authentication"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class StudentRegistrationView(generics.CreateAPIView):
    serializer_class = StudentRegistrationSerializer

    @swagger_auto_schema(tags=["Authentication"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ProfessorRegistrationView(generics.CreateAPIView):
    serializer_class = ProfessorRegistrationSerializer

    @swagger_auto_schema(tags=["Authentication"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LoginView(APIView):
    @swagger_auto_schema(tags=["Authentication"], request_body=LoginSerializer)
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user_id": user.id,
                "username": user.username,
            }
        )


class ExternalLoginView(APIView):
    """
    POST: {
        "username": str,
        "password": str,
        "university_code": str
    }
    """

    @swagger_auto_schema(
        tags=["Authentication"],
        request_body=ExternalLoginSerializer,
        operation_description="Логин через внешний университетский API. Пользователь выбирает университет, вводит логин и пароль. После успешной аутентификации студент и все связанные сущности (факультет, департамент, группа) синхронизируются в локальной базе.",
    )
    def post(self, request, *args, **kwargs):
        serializer = ExternalLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        university_code = serializer.validated_data["university_code"]

        # 1. Университет
        try:
            uni_url_obj = UniversityUrlsModel.objects.get(code=university_code)
        except UniversityUrlsModel.DoesNotExist:
            return Response(
                {"success": False, "error": "Университет не найден"}, status=400
            )
        api_url = uni_url_obj.api_url.rstrip("/") + "/"

        # 2. Внешний логин
        login_url = api_url + "auth/login"
        login_resp = requests.post(
            login_url, json={"login": username, "password": password}
        )
        if not login_resp.ok or not login_resp.json().get("success"):
            return Response(
                {
                    "success": False,
                    "error": "Неверные данные для входа или ошибка внешнего API",
                },
                status=401,
            )
        token = login_resp.json()["data"]["token"]

        # 3. Получить данные студента
        me_url = api_url + "account/me"
        me_resp = requests.get(me_url, headers={"Authorization": f"Bearer {token}"})
        if not me_resp.ok or not me_resp.json().get("success"):
            return Response(
                {"success": False, "error": "Ошибка получения данных студента"},
                status=400,
            )
        student_data = me_resp.json()["data"]

        # 🔐 Start atomic block
        with transaction.atomic():
            # 4. Факультет
            faculty_data = student_data.get("faculty")
            faculty_obj = None

            if faculty_data:
                faculty_obj, _ = FacultyModel.objects.get_or_create(
                    code=faculty_data.get("code", ""),
                    university=uni_url_obj.university,
                    defaults={"name": faculty_data.get("name", "")},
                )
                if faculty_obj.name != faculty_data.get("name", ""):
                    faculty_obj.name = faculty_data.get("name", "")
                    faculty_obj.save()

            # 5. Департамент
            department_data = student_data.get("specialty")
            department_obj = None
            if department_data and faculty_obj:
                department_obj, _ = DepartmentModel.objects.get_or_create(
                    code=department_data.get("code", ""),
                    faculty=faculty_obj,
                    defaults={"name": department_data.get("name", "")},
                )
                if department_obj.name != department_data.get("name", ""):
                    department_obj.name = department_data.get("name", "")
                    department_obj.save()

            # 6. Группа
            group_data = student_data.get("group")
            group_obj = None
            if group_data and department_obj:
                group_obj, _ = GroupModel.objects.get_or_create(
                    name=group_data.get("name", ""),
                    university=uni_url_obj.university,
                    department=department_obj,
                )

            # 7. Пользователь и студент
            user_model = get_user_model()
            user, created = user_model.objects.get_or_create(username=username)
            if created:
                user.set_password(password)
                user.save()

            # ✅ Convert timestamp to date
            birth_ts = student_data.get("birth_date")
            birth_date = None
            if isinstance(birth_ts, int):
                birth_date = datetime.datetime.fromtimestamp(
                    birth_ts, datetime.UTC
                ).date()

            student_profile, _ = StudentProfileModel.objects.update_or_create(
                user=user,
                defaults={
                    "student_id_number": student_data.get(
                        "student_id_number", username
                    ),
                    "image_url": student_data.get("image", ""),
                    "first_name": student_data.get("first_name", ""),
                    "second_name": student_data.get("second_name", ""),
                    "third_name": student_data.get("third_name", ""),
                    "full_name": student_data.get("full_name", ""),
                    "short_name": student_data.get("short_name", ""),
                    "birth_date": birth_date,
                    "passport_pin": student_data.get("passport_pin", ""),
                    "passport_number": student_data.get("passport_number", ""),
                    "email": student_data.get("email", ""),
                    "phone": student_data.get("phone", ""),
                    "gender_code": (student_data.get("gender") or {}).get("code", ""),
                    "gender_name": (student_data.get("gender") or {}).get("name", ""),
                    "university": uni_url_obj.university,
                    "department": department_obj.name if department_obj else None,
                },
            )
            # 8. Привязка студента к группе
            if group_obj:
                from students.models import StudentsGroupModel

                StudentsGroupModel.objects.get_or_create(
                    student=student_profile, group=group_obj
                )
            # 9. Получить и сохранить предметы
            subjects_url = api_url + "education/subjects"
            subjects_resp = requests.get(
                subjects_url, headers={"Authorization": f"Bearer {token}"}
            )

            if subjects_resp.ok and subjects_resp.json().get("success"):
                subject_entries = subjects_resp.json()["data"]
                for entry in subject_entries:
                    subj_data = entry.get("subject")
                    if not subj_data:
                        continue  # skip if no subject info

                    subject_obj, _ = SubjectModel.objects.get_or_create(
                        code=subj_data["code"],
                        university=uni_url_obj.university,
                        department=department_obj,
                        defaults={"name": subj_data["name"]},
                    )

                    # Связь студент–предмет
                    StudentSubjectModel.objects.get_or_create(
                        student=student_profile,
                        subject=subject_obj,
                    )
            # 11. Fetch and sync schedule
            schedule_url = api_url + "education/schedule"
            schedule_resp = requests.get(
                schedule_url, headers={"Authorization": f"Bearer {token}"}
            )
            if schedule_resp.ok and schedule_resp.json().get("success"):
                timetable_obj, _ = StudentTimetableModel.objects.get_or_create(
                    group=group_obj
                )

                for item in schedule_resp.json()["data"]:
                    subj = item["subject"]
                    subject_obj, _ = SubjectModel.objects.get_or_create(
                        code=subj["code"],
                        university=uni_url_obj.university,
                        department=department_obj,
                        defaults={"name": subj["name"]},
                    )

                    # 1. Professor
                    prof_name = item.get("employee", {}).get("name", "")
                    prof_id = item.get("employee", {}).get("id", "")
                    if prof_name:
                        prof_user, _ = get_user_model().objects.get_or_create(
                            username=prof_name
                        )

                        professor_obj, _ = ProfessorProfileModel.objects.get_or_create(
                            user=prof_user,
                            university=uni_url_obj.university,
                            defaults={"name": prof_name, "professor_id": prof_id},
                        )

                        # 3. Link professor to subject
                        if professor_obj:
                            ProfessorsSubjectModel.objects.get_or_create(
                                professor=professor_obj, subject=subject_obj
                            )

                    else:
                        professor_obj = None

                    # 2. Time & Day
                    lesson_date_ts = item.get("lesson_date")
                    if lesson_date_ts:
                        dt = datetime.datetime.fromtimestamp(
                            lesson_date_ts, tz=datetime.UTC
                        )
                        weekday = dt.strftime("%A").lower()  # e.g., "monday"

                        start_time = item.get("lessonPair", {}).get(
                            "start_time", "00:00"
                        )
                        end_time = item.get("lessonPair", {}).get("end_time", "00:00")

                        room = item.get("auditorium", {}).get("name", "")

                        if professor_obj:
                            StudentTimeTablesubjectModel.objects.get_or_create(
                                timetable=timetable_obj,
                                subject=subject_obj,
                                professor=professor_obj,
                                day=weekday,
                                start_time=start_time,
                                end_time=end_time,
                                room=room,
                            )
            refresh = RefreshToken.for_user(user)

        # 🟢 Return after atomic block
        return Response(
            {
                "success": True,
                "student_profile": {
                    "first_name": student_profile.first_name,
                    "second_name": student_profile.second_name,
                    "third_name": student_profile.third_name,
                    "full_name": student_profile.full_name,
                    "short_name": student_profile.short_name,
                    "student_id_number": student_profile.student_id_number,
                    "email": student_profile.email,
                },
                "faculty": faculty_obj.name if faculty_obj else None,
                "department": department_obj.name if department_obj else None,
                "group": group_obj.name if group_obj else None,
                "token": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user_id": user.id,
                    "username": user.username,
                },
            }
        )


class FetchUpdateUniversityUrlsView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(auto_schema=None)
    def post(self, request, *args, **kwargs):
        result = UniversityUrlsModel.fetch_and_save_from_api(None)
        return Response(result)

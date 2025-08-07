from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg import openapi

# from django.templatetags.static import static
from django.urls import reverse

UNFOLD = {
    "SITE_TITLE": "Imtihon - Educational Management System",
    "SITE_HEADER": "Imtihon Admin",
    "SITE_URL": "/",
    "SITE_SYMBOL": "school",
    "SITE_DROPDOWN": [
        {
            "icon": "school",
            "title": _("Imtihon System"),
            "link": "/",
        },
    ],
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_BACK_BUTTON": False,
    # "STYLES": [
    #     lambda request: static("/css/style.css"),
    # ],
    # "SCRIPTS": [
    #     lambda request: static("js/script.js"),
    # ],
    "BORDER_RADIUS": "10px",
    "COLORS": {
        "base": {
            "50": "250 252 255",  # #FAFCFF – Almost pure white with a hint of blue
            "100": "240 245 255",  # #F0F5FF – Clean white-blue
            "200": "220 235 255",  # #DCEBFF – Pale sky blue
            "300": "195 220 255",  # #C3DCFF – Very light blue
            "400": "160 200 255",  # #A0C8FF – Light blue
            "500": "120 180 255",  # #78B4FF – Main light blue
            "600": "90 150 230",  # #5A96E6 – Bright usable blue
            "700": "65 120 200",  # #4178C8 – Mid-dark blue
            "800": "45 90 160",  # #2D5AA0 – Deep blue
            "900": "25 50 110",  # #19326E – Dark navy
            "950": "15 30 60",  # #0F1E3C – Ultra dark blue
        },
        "primary": {
            "50": "245 250 255",  # #F5FAFF – Icy white-blue
            "100": "225 240 255",  # #E1F0FF – Soft pastel blue
            "200": "180 220 255",  # #B4DCFF – Gentle light blue
            "300": "140 200 255",  # #8CC8FF – Brighter sky
            "400": "100 180 255",  # #64B4FF – CTA blue
            "500": "60 150 255",  # #3C96FF – Bold primary
            "600": "45 120 220",  # #2D78DC – Strong link/nav blue
            "700": "30 95 185",  # #1E5FB9 – Dense blue
            "800": "20 70 150",  # #144696 – Navy-leaning
            "900": "10 40 100",  # #0A2864 – Ultra deep blue
            "950": "5 20 50",  # #051432 – Almost black navy
        },
    },
    "SIDEBAR": {
        "show_search": False,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("Навигация"),
                "separator": False,
                "collapsible": False,
                "items": [
                    {
                        "title": _("Панель управления"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "title": _("🏫 Университет"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Университеты"),
                        "icon": "school",
                        "link": reverse_lazy(
                            "admin:university_universitymodel_changelist"
                        ),
                        "permission": lambda request: request.user.is_staff,
                    },
                    {
                        "title": _("Факультеты"),
                        "icon": "business",
                        "link": reverse_lazy(
                            "admin:university_facultymodel_changelist"
                        ),
                        "permission": lambda request: request.user.is_staff,
                    },
                    {
                        "title": _("Кафедры"),
                        "icon": "apartment",
                        "link": reverse_lazy(
                            "admin:university_departmentmodel_changelist"
                        ),
                        "permission": lambda request: request.user.is_staff,
                    },
                    {
                        "title": _("Группы"),
                        "icon": "group",
                        "link": reverse_lazy("admin:university_groupmodel_changelist"),
                        "permission": lambda request: request.user.is_staff,
                    },
                    {
                        "title": _("Предметы"),
                        "icon": "book",
                        "link": reverse_lazy(
                            "admin:university_subjectmodel_changelist"
                        ),
                        "permission": lambda request: request.user.is_staff,
                    },
                    {
                        "title": _("Университет URL'лари"),
                        "icon": "link",
                        "link": reverse_lazy(
                            "admin:accounts_universityurlsmodel_changelist"
                        ),
                        "permission": lambda request: request.user.is_staff,
                    },
                ],
            },
            {
                "title": _("👨‍🏫 Преподаватели"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Профили преподавателей"),
                        "icon": "person",
                        "link": reverse_lazy(
                            "admin:professors_professorprofilemodel_changelist"
                        ),
                        "permission": lambda request: request.user.is_staff,
                    },
                    {
                        "title": _("Предметы преподавателей"),
                        "icon": "assignment",
                        "link": reverse_lazy(
                            "admin:professors_professorssubjectmodel_changelist"
                        ),
                        "permission": lambda request: request.user.is_staff,
                    },
                ],
            },
            {
                "title": _("👨‍🎓 Студенты"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Профили студентов"),
                        "icon": "person",
                        "link": reverse_lazy(
                            "admin:students_studentprofilemodel_changelist"
                        ),
                        "permission": lambda request: request.user.is_staff,
                    },
                    {
                        "title": _("Группы студентов"),
                        "icon": "group",
                        "link": reverse_lazy(
                            "admin:students_studentsgroupmodel_changelist"
                        ),
                        "permission": lambda request: request.user.is_staff,
                    },
                    {
                        "title": _("Расписание студентов"),
                        "icon": "schedule",
                        "link": reverse_lazy(
                            "admin:students_studenttimetablemodel_changelist"
                        ),
                        "permission": lambda request: request.user.is_staff,
                    },
                    {
                        "title": _("Предметы расписания"),
                        "icon": "book",
                        "link": reverse_lazy(
                            "admin:students_studenttimetablesubjectmodel_changelist"
                        ),
                        "permission": lambda request: request.user.is_staff,
                    },
                    {
                        "title": _("Сессии студентов"),
                        "icon": "computer",
                        "link": reverse_lazy(
                            "admin:students_studentsessionmodel_changelist"
                        ),
                        "permission": lambda request: request.user.is_staff,
                    },
                    {
                        "title": _("Ответы студентов"),
                        "icon": "quiz",
                        "link": reverse_lazy(
                            "admin:students_studentanswermodel_changelist"
                        ),
                        "permission": lambda request: request.user.is_staff,
                    },
                    # {
                    #     "title": _("Доказательства списывания"),
                    #     "icon": "warning",
                    #     "link": reverse_lazy(
                    #         "admin:students_cheatingevidencemodel_changelist"
                    #     ),
                    #     "permission": lambda request: request.user.is_staff,
                    # },
                ],
            },
            {
                "title": _("📚 Курсы"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Курсы"),
                        "icon": "library_books",
                        "link": reverse_lazy("admin:course_coursemodel_changelist"),
                        "permission": lambda request: request.user.is_staff,
                    },
                    {
                        "title": _("Разделы курсов"),
                        "icon": "folder",
                        "link": reverse_lazy(
                            "admin:course_coursesectionmodel_changelist"
                        ),
                        "permission": lambda request: request.user.is_staff,
                    },
                    {
                        "title": _("Уроки курсов"),
                        "icon": "article",
                        "link": reverse_lazy(
                            "admin:course_courselessonmodel_changelist"
                        ),
                        "permission": lambda request: request.user.is_staff,
                    },
                ],
            },
            {
                "title": _("📝 Задания"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Задания"),
                        "icon": "assignment",
                        "link": reverse_lazy(
                            "admin:assignments_assignmentmodel_changelist"
                        ),
                        "permission": lambda request: request.user.is_staff,
                    },
                    {
                        "title": _("Вопросы"),
                        "icon": "quiz",
                        "link": reverse_lazy(
                            "admin:assignments_questionmodel_changelist"
                        ),
                        "permission": lambda request: request.user.is_staff,
                    },
                    {
                        "title": _("Варианты ответов"),
                        "icon": "list",
                        "link": reverse_lazy(
                            "admin:assignments_questionchoicemodel_changelist"
                        ),
                        "permission": lambda request: request.user.is_staff,
                    },
                ],
            },
        ],
    },
}


def dashboard_callback(request, context):
    """
    Callback to prepare custom variables for index template which is used as dashboard
    template. It can be overridden in application by creating custom admin/index.html.
    """
    context.update(
        {
            "sample": "example",  # this will be injected into templates/admin/index.html
        }
    )
    return context


import logging.config


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "debug.log",  # Log fayl nomi
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "DEBUG",
            "propagate": True,
        },
        "celery": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


def setup_logging():
    logging.config.dictConfig(LOGGING)


schema_view = get_schema_view(
    openapi.Info(
        title="Imtihon Educational Management System",
        default_version="v1",
        description="API for Imtihon Educational Management System",
        terms_of_service="https:#www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@imtihon.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

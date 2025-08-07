# schema_urls.py

from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
import os


schema_view = get_schema_view(
    openapi.Info(
        title="Imtihon API",
        default_version="v1",
        description="Here to use these endpoints use domain + api + the endpoint from swagger docs "
        "e.g https://imtihon.divspan.uz/imtihon/crud/api/auth/external-login/ for students to login by hemis username and password",
    ),
    public=True,
    url=f"http://{os.environ.get("HOST", "localhost")}",
    permission_classes=(permissions.AllowAny,),
    patterns=[
        path("imtihon/crud/api/course/", include("course.urls")),
        path("imtihon/crud/api/assignments/", include("assignments.urls")),
        path("imtihon/crud/api/university/", include("university.urls")),
        path("imtihon/crud/api/students/", include("students.urls")),
        # path("api/professors/", include("professors.urls")),
        path("imtihon/crud/api/auth/", include("accounts.urls")),
    ],
)

urlpatterns = [
    path(
        "",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]

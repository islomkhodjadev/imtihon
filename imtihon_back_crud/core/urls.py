# urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("imtihon/crud/admin/", admin.site.urls),
    path("imtihon/crud/api/course/", include("course.urls")),
    path(
        "imtihon/crud/api/assignments/", include("assignments.urls")
    ),  # whatever you use
    path("imtihon/crud/api/university/", include("university.urls")),
    path("imtihon/crud/api/students/", include("students.urls")),
    # path("api/professors/", include("professors.urls")),
    path("imtihon/crud/api/auth/", include("accounts.urls")),
    # 🚨 Import only this: routes limited by patterns in schema_urls.py
    path("imtihon/crud/docs/", include("core.schema_urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

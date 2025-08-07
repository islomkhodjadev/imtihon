from django.urls import path
from .views import (
    UniversityRegistrationView,
    StudentRegistrationView,
    ProfessorRegistrationView,
    LoginView,
    FetchUpdateUniversityUrlsView,
    ExternalLoginView,
)

urlpatterns = [
    path(
        "register/university/",
        UniversityRegistrationView.as_view(),
        name="register-university",
    ),
    # path("register/student/", StudentRegistrationView.as_view(), name="register-student"),
    path(
        "register/professor/",
        ProfessorRegistrationView.as_view(),
        name="register-professor",
    ),
    path("login/", LoginView.as_view(), name="login"),
    path(
        "fetch-update-university-urls/",
        FetchUpdateUniversityUrlsView.as_view(),
        name="fetch-update-university-urls",
    ),
    path(
        "external-login/",
        ExternalLoginView.as_view(),
        name="external-login",
    ),
]

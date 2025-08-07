from unfold.admin import ModelAdmin
from .models import (
    UniversityModel,
    FacultyModel,
    DepartmentModel,
    GroupModel,
    SubjectModel,
)
from django.contrib import admin


@admin.register(UniversityModel)
class UniversityModelAdmin(ModelAdmin):
    list_display = ("id", "name", "location", "number", "email", "website", "user")
    search_fields = ("name", "location", "number", "email", "website", "user__username")
    list_filter = ("location",)
    ordering = ("name",)
    readonly_fields = ("id",)


@admin.register(FacultyModel)
class FacultyModelAdmin(ModelAdmin):
    list_display = ("id", "name", "code", "university")
    search_fields = ("name", "code", "university__name")
    list_filter = ("university",)
    ordering = ("university", "name")
    readonly_fields = ("id",)


@admin.register(DepartmentModel)
class DepartmentModelAdmin(ModelAdmin):
    list_display = ("id", "name", "code", "faculty")
    search_fields = ("name", "code", "faculty__name")
    list_filter = ("faculty",)
    ordering = ("faculty", "name")
    readonly_fields = ("id",)


@admin.register(GroupModel)
class GroupModelAdmin(ModelAdmin):
    list_display = ("id", "name", "university", "department")
    search_fields = ("name", "university__name", "department__name")
    list_filter = ("university", "department")
    ordering = ("university", "department", "name")
    readonly_fields = ("id",)


@admin.register(SubjectModel)
class SubjectModelAdmin(ModelAdmin):
    list_display = (
        "id",
        "name",
        "university",
        "department",
    )
    search_fields = (
        "name",
        "university__name",
        "department__name",
    )
    list_filter = ("university", "department")
    ordering = ("university", "department", "name")
    readonly_fields = ("id",)

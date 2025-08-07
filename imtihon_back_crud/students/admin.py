from unfold.admin import ModelAdmin, TabularInline
from .models import (
    StudentProfileModel,
    StudentsGroupModel,
    StudentTimetableModel,
    StudentTimeTablesubjectModel,
    CheatingEvidenceModel,
    StudentAnswerModel,
    StudentSessionModel,
)
from django.contrib import admin


class StudentTimeTablesubjectModelInline(TabularInline):
    model = StudentTimeTablesubjectModel
    extra = 1  # Number of empty forms to display
    fields = ("subject", "professor", "day", "start_time", "end_time", "room")
    ordering = ("day", "start_time")


from django.utils.html import format_html
import mimetypes


class CheatingEvidenceModelInline(TabularInline):
    model = CheatingEvidenceModel
    extra = 1
    fields = ("type", "evidence_file", "preview")  # Add preview field
    readonly_fields = ("type", "preview")  # make both read-only

    def preview(self, instance):
        if not instance.evidence_file:
            return "-"

        file_url = instance.evidence_file.url
        mime_type, _ = mimetypes.guess_type(file_url)

        if mime_type:
            if mime_type.startswith("image/"):
                return format_html(
                    f'<img src="{file_url}" style="max-height: 150px;" />'
                )
            elif mime_type.startswith("audio/"):
                return format_html(
                    f'<audio controls><source src="{file_url}" type="{mime_type}">Your browser does not support the audio tag.</audio>'
                )

        return format_html(f'<a href="{file_url}" target="_blank">Download File</a>')

    preview.short_description = "Preview"


class StudentsGroupInline(TabularInline):
    model = StudentsGroupModel
    extra = 0


@admin.register(StudentProfileModel)
class StudentProfileAdmin(ModelAdmin):
    list_display = (
        "id",
        "user",
        "student_id_number",
        "first_name",
        "second_name",
        "third_name",
        "full_name",
        "short_name",
        "birth_date",
        "email",
        "university",
        "image_url",
    )
    search_fields = (
        "student_id_number",
        "first_name",
        "second_name",
        "third_name",
        "full_name",
        "email",
    )
    list_filter = ("university",)
    inlines = [StudentsGroupInline]
    readonly_fields = ("id",)


@admin.register(StudentsGroupModel)
class StudentsGroupModelAdmin(ModelAdmin):
    list_display = ("id", "student", "group")
    search_fields = ("student__student_id", "group__number")
    list_filter = ("group",)
    ordering = ("group", "student")
    readonly_fields = ("id",)


@admin.register(StudentTimetableModel)
class StudentTimetableModelAdmin(ModelAdmin):
    inlines = [StudentTimeTablesubjectModelInline]
    list_display = ("id", "group", "get_subject_count")
    search_fields = ("group__number",)
    ordering = ("group",)
    readonly_fields = ("id",)

    def get_subject_count(self, obj):
        return obj.subjects.count()

    get_subject_count.short_description = "Number of Subjects"


@admin.register(StudentSessionModel)
class StudentSessionModelAdmin(ModelAdmin):
    inlines = [CheatingEvidenceModelInline]
    list_display = (
        "id",
        "student",
        "assignment",
        "start_time",
        "end_time",
        "cheating_score",
        "grade",
        "get_evidence_count",
    )
    list_filter = ("assignment__subject", "start_time", "cheating_score", "grade")
    search_fields = ("student__student_id", "assignment__description")
    ordering = ("student", "assignment", "start_time")
    readonly_fields = ("id", "start_time")

    def get_evidence_count(self, obj):
        return obj.cheating_evidence.count()

    get_evidence_count.short_description = "Evidence Count"


@admin.register(StudentTimeTablesubjectModel)
class StudentTimeTablesubjectModelAdmin(ModelAdmin):
    list_display = (
        "id",
        "timetable",
        "subject",
        "professor",
        "day",
        "start_time",
        "end_time",
        "room",
    )
    list_filter = ("day", "subject", "timetable__group", "professor")
    search_fields = ("subject__name", "professor__professor_id", "room")
    ordering = ("timetable__group", "day", "start_time")
    readonly_fields = ("id",)


# @admin.register(CheatingEvidenceModel)
# class CheatingEvidenceModelAdmin(ModelAdmin):
#     list_display = ("id", "session", "type", "evidence_file")
#     list_filter = ("type", "session__assignment__subject")
#     search_fields = ("session__student__student_id", "type")
#     ordering = ("session", "type")
#     readonly_fields = ("id", "session")


@admin.register(StudentAnswerModel)
class StudentAnswerModelAdmin(ModelAdmin):
    list_display = (
        "id",
        "session",
        "question",
        "choice",
        "true_false_answer",
        "text_answer",
    )
    search_fields = (
        "session__student__student_id",
        "question__question",
        "choice__choice",
    )
    list_filter = ("session", "question")
    ordering = ("session", "question")
    readonly_fields = ("id",)

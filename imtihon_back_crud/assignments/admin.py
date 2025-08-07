from unfold.admin import ModelAdmin, TabularInline
from .models import (
    AssignmentModel,
    QuestionModel,
    QuestionChoiceModel,
    AssignmentAttachmentsModel,
    AssignmentsGroupModel,
)
from django.contrib import admin


class AssignmentAttachmentsModelInline(TabularInline):
    model = AssignmentAttachmentsModel
    extra = 1
    fields = ("attachment_file",)


@admin.register(AssignmentModel)
class AssignmentModelAdmin(ModelAdmin):
    inlines = [AssignmentAttachmentsModelInline]
    list_display = (
        "id",
        "type",
        "subject",
        "professor",
        "start_time",
        "end_time",
        "max_grade",
        "description",
    )
    search_fields = ("subject__name", "professor__professor_id", "description")
    list_filter = ("type", "subject", "professor", "start_time", "end_time")
    ordering = ("subject", "start_time")
    readonly_fields = ("id",)


@admin.register(QuestionModel)
class QuestionModelAdmin(ModelAdmin):
    list_display = (
        "id",
        "assignment",
        "type",
        "question",
        "text_answer",
        "true_false_answer",
    )
    search_fields = ("assignment__subject__name", "question")
    list_filter = ("assignment", "type")
    ordering = ("assignment", "type")
    readonly_fields = ("id",)


@admin.register(QuestionChoiceModel)
class QuestionChoiceModelAdmin(ModelAdmin):
    list_display = ("id", "question", "choice", "is_correct")
    search_fields = ("question__question", "choice")
    list_filter = ("question", "is_correct")
    ordering = ("question",)
    readonly_fields = ("id",)


@admin.register(AssignmentAttachmentsModel)
class AssignmentAttachmentsModelAdmin(ModelAdmin):
    list_display = ("id", "assignment", "attachment_file")
    search_fields = ("assignment__description",)
    list_filter = ("assignment",)
    ordering = ("assignment",)
    readonly_fields = ("id",)


@admin.register(AssignmentsGroupModel)
class AssignmentsGroupModelAdmin(ModelAdmin):
    list_display = ("id", "assignment", "group")
    search_fields = ("assignment__description", "group__number")
    list_filter = ("assignment", "group")
    ordering = ("assignment", "group")
    readonly_fields = ("id",)

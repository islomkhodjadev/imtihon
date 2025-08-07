from unfold.admin import ModelAdmin
from .models import (
    CourseModel,
    CourseSectionModel,
    CourseLessonModel,
    CourseAttachmentsModel,
)
from django.contrib import admin


class CourseAttachmentsModelInline(admin.TabularInline):
    model = CourseAttachmentsModel
    extra = 1
    fields = ("attachment_file",)


@admin.register(CourseModel)
class CourseModelAdmin(ModelAdmin):
    list_display = (
        "id",
        "name",
        "subject",
        "description",
        "intro_image",
    )
    search_fields = (
        "name",
        "subject__name",
        "description",
    )
    list_filter = ("subject",)
    ordering = ("name",)
    readonly_fields = ("id",)
    inlines = [CourseAttachmentsModelInline]


@admin.register(CourseSectionModel)
class CourseSectionModelAdmin(ModelAdmin):
    list_display = ("id", "name", "course", "description", "intro_video", "intro_image")
    search_fields = ("name", "course__name", "description")
    list_filter = ("course",)
    ordering = ("course", "name")
    readonly_fields = ("id",)


@admin.register(CourseLessonModel)
class CourseLessonModelAdmin(ModelAdmin):
    list_display = ("id", "name", "section", "text", "video", "image")
    search_fields = ("name", "section__name", "text")
    list_filter = ("section",)
    ordering = ("section", "name")
    readonly_fields = ("id",)

from unfold.admin import ModelAdmin
from .models import ProfessorProfileModel, ProfessorsSubjectModel
from django.contrib import admin

@admin.register(ProfessorProfileModel)
class ProfessorProfileModelAdmin(ModelAdmin):
    list_display = ("id", "professor_id", "user", "university")
    search_fields = ("professor_id", "user__username", "university__name")
    list_filter = ("university",)
    ordering = ("university", "professor_id")
    readonly_fields = ("id",)

@admin.register(ProfessorsSubjectModel)
class ProfessorsSubjectModelAdmin(ModelAdmin):
    list_display = ("id", "professor", "subject")
    search_fields = ("professor__professor_id", "subject__name")
    list_filter = ("professor", "subject")
    ordering = ("professor", "subject")
    readonly_fields = ("id",)

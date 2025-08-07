from unfold.admin import ModelAdmin
from django.contrib import admin
from accounts.models import UniversityUrlsModel
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from unfold.decorators import action
from django.contrib.auth import get_user_model

# admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group

from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


@admin.register(UniversityUrlsModel)
class UniversityUrlsUnfoldAdmin(ModelAdmin):
    list_display = (
        "id",
        "name",
        "code",
        "api_url",
        "student_url",
        "employee_url",
        "university",
        # "fetch_update_button",
    )
    search_fields = ("name", "code")
    list_filter = ("university",)
    readonly_fields = ("id",)

    actions_list = ["fetch_update_from_api_action"]

    @action(
        description=_("Обновить из API"),
        icon="refresh",
    )
    def fetch_update_from_api_action(self, request):
        result = UniversityUrlsModel.fetch_and_save_from_api(None)
        self.message_user(request, f"Результат обновления: {result}")
        from django.shortcuts import redirect

        changelist_url = reverse("admin:accounts_universityurlsmodel_changelist")
        return redirect(changelist_url)

    def fetch_update_button(self, obj):
        url = reverse("admin:accounts_universityurlsmodel_fetch_update")
        button_html = f"""
        <a href=\"{url}\" class=\"bg-primary-600 border border-transparent focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 font-medium hover:bg-primary-700 inline-flex items-center px-3 py-2 rounded-md shadow-sm text-sm text-white\">
            {_("Обновить из API")}
        </a>
        """
        return format_html(button_html)

    fetch_update_button.short_description = _("Обновить из API")
    fetch_update_button.allow_tags = True

    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        custom_urls = [
            path(
                "fetch-update/",
                self.admin_site.admin_view(self.fetch_update_view),
                name="accounts_universityurlsmodel_fetch_update",
            ),
        ]
        return custom_urls + urls

    def fetch_update_view(self, request):
        result = UniversityUrlsModel.fetch_and_save_from_api(None)
        self.message_user(request, f"Результат обновления: {result}")
        from django.shortcuts import redirect

        return redirect("..")


from .models import APIKey


@admin.register(APIKey)
class APIKeyAdmin(ModelAdmin):
    list_display = ("name", "key", "is_active", "created_at", "last_used_at")
    readonly_fields = ("key", "created_at", "last_used_at")
    search_fields = ("name", "key")

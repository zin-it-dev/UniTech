from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Permission

from .models import User, StudentProxy, Course, Category, Tag
from .forms import UserChangeForm, UserCreationForm
from .inlines import StudentInline, TagCourseInline


class BaseAdmin(admin.ModelAdmin):
    empty_value_display = "-Unknown-"
    list_display = ["is_active", "date_created", "date_updated"]
    ordering = ["-date_created"]
    list_editable = ["is_active"]
    list_filter = ["is_active"]
    date_hierarchy = "date_created"
    list_per_page = 10


class CommonAdmin(BaseAdmin):
    prepopulated_fields = {"slug": ["label"]}


class UserAdmin(BaseUserAdmin, BaseAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ["email", "role", "is_active", "last_login"]
    date_hierarchy = "date_joined"
    list_editable = ["is_active"]
    search_fields = ["email", "first_name", "last_name"]
    list_filter = ["is_superuser", "is_active", "is_staff"]

    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        (
            "Personal Info",
            {
                "fields": [
                    "first_name",
                    "last_name",
                    "is_active",
                    "date_joined",
                    "last_login",
                ]
            },
        ),
        ("Permissions", {"fields": ["is_superuser", "is_staff", "user_permissions"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "password",
                    "confirm_password",
                    "first_name",
                    "last_name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                ],
            },
        ),
    ]
    ordering = ["email", "first_name", "last_name"]
    filter_horizontal = ["user_permissions"]


class StudentAdmin(UserAdmin):
    inlines = [StudentInline]
    list_display = ["full_name", "is_active", "last_login"]


class CategoryAdmin(CommonAdmin):
    list_display = ["label"] + CommonAdmin.list_display


class TagAdmin(CommonAdmin):
    list_display = ["label"] + CommonAdmin.list_display


class CourseAdmin(BaseAdmin):
    inlines = [TagCourseInline]
    list_display = ["title"] + BaseAdmin.list_display
    prepopulated_fields = {"slug": ["title"]}
    exclude = ["tags"]


admin.site.register(User, UserAdmin)
admin.site.register(StudentProxy, StudentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Permission)

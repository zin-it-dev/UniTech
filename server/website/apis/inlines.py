from django.contrib import admin

from .models import Student, Course


class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False


class TagCourseInline(admin.TabularInline):
    model = Course.tags.through

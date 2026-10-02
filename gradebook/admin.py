from django.contrib import admin

from .models import Course, Result, Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("index_number", "first_name", "last_name", "email")
    search_fields = ("index_number", "first_name", "last_name", "email")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "title")
    search_fields = ("code", "title")


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "marks")
    list_filter = ("course",)
    search_fields = ("student__index_number", "student__last_name", "course__code")

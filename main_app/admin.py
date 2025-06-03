from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Staff, Student, Course, Book, IssuedBook, Library, Subject, Session

# Custom admin for CustomUser
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    ordering = ('email',)
    list_display = ('email', 'username', 'user_type', 'is_active', 'is_staff')
    search_fields = ('email', 'username')
    list_filter = ('user_type', 'is_active', 'is_staff')

# Register other models with default admin
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'admin')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'admin', 'course')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author')

@admin.register(IssuedBook)
class IssuedBookAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'student', 'issue_date', 'return_date')

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'course', 'staff')

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_year', 'end_year')

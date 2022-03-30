from .models import ClassTest, User, Student, StudentMarks, Teacher, StudentsInClass, LiveClass
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
# Register your models here.

admin.site.register(LiveClass)
admin.site.register(ClassTest)
admin.site.register(User, UserAdmin)
admin.site.register(StudentMarks)
admin.site.register(Teacher)
admin.site.register(StudentsInClass)
admin.site.register(Student)

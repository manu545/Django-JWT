from django.contrib import admin

from . models import student, teacher

# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    fields = ['name', 'username', 'teacher', 'password']

class TeacherAdmin(admin.ModelAdmin):
    fields = ['name', 'subject', 'username', 'password']

admin.site.register(student, StudentAdmin)
admin.site.register(teacher, TeacherAdmin)
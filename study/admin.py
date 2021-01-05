from django.contrib import admin
from .models import StudentInfo, Faculty, Department, Subject, Gender


# Register your models here.
admin.site.register(StudentInfo)
admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(Subject)
admin.site.register(Gender)
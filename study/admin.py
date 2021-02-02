from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User, Faculty, Department, Subject, Gender, Teach


# Register your models here.


admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(Subject)
admin.site.register(Gender)
admin.site.register(Teach)
admin.site.register(User)

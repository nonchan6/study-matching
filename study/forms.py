from django import forms
from .models import StudentInfo


class TestForm(forms.Form):
    text = forms.CharField(label='名前')
    num = forms.IntegerField(label='学年')


class StudentInfoAdd(forms.ModelForm):
    class Meta:
        model = StudentInfo
        fields = ['name', 'student_number', 'gender', 'department', 'year']

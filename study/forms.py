from django import forms
from .models import Faculty, Subject, User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            # placeholderにフィールドのラベルを入れる
            field.widget.attrs['placeholder'] = field.label


class UserCreateForm(UserCreationForm):
    """ユーザー登録用フォーム"""

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email


"""
   class TestForm(forms.Form):
       text = forms.CharField(label='名前')
       num = forms.IntegerField(label='学年')

User = get_user_model()

class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        if User.USERNAME_FIELD == 'email':
            fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

"""

"""
class StudentInfoAdd(forms.ModelForm):
    faculty = forms.ModelChoiceField(
        label='学部',
        queryset=Faculty.objects,
        required=False
    )

    teach = forms.ModelChoiceField(
        label='教えられる科目',
        queryset=Subject.objects,
        required=False
    )

    class Meta:
        model = StudentInfo
        fields = '__all__'

    field_order = ('name', 'student_number', 'gender',
                   'faculty', 'department', 'year')
"""

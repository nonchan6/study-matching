from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone

# Create your models here.


class Faculty(models.Model):
    name = models.CharField('学部名', max_length=255)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField('学科名', max_length=255)
    faculty = models.ForeignKey(
        Faculty, verbose_name='学部', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField('科目名', max_length=255)
    department = models.ForeignKey(
        Department, verbose_name='学科', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Gender(models.Model):
    name = models.CharField('性別', max_length=255)

    def __str__(self):
        return self.name


class Langage(models.Model):
    name = models.CharField('母国語', max_length=255)

    def _str_(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='メールアドレス',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    # username_validator = UnicodeUsernameValidator()

    username = models.CharField('ユーザネーム', max_length=255)
    student_number = models.IntegerField('学籍番号', default=0)
    gender = models.ForeignKey(
        Gender, verbose_name='性別', on_delete=models.SET_NULL, null=True)
    langague = models.ForeignKey(
        Langage, verbose_name='母国語', on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(
        Department,
        verbose_name='学科',
        on_delete=models.SET_NULL,
        null=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['date_of_birth']

    """
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
    """

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Teach(models.Model):
    subject = models.ForeignKey(
        Subject, verbose_name='教える教科', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(
        User, verbose_name='ユーザ', on_delete=models.CASCADE)

    def __str__(self):
        return self.subject

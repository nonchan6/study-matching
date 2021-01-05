from django.db import models
from django.utils import timezone

# Create your models here.
class Faculty(models.Model):
    name = models.CharField('学部名', max_length=255)

    def __str__(self):
        return self.name

class Department(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    name = models.CharField('学科名', max_length=255)

    def __str__(self):
        return self.name

class Subject(models.Model):
    faculty = models.ForeignKey(Faculty,on_delete=models.CASCADE)
    name = models.CharField('科目名', max_length=255)

    def __str__(self):
        return self.name

class Gender(models.Model):
    gender = models.CharField('性別', max_length=255)

    def __str__(self):
        return self.gender

class StudentInfo(models.Model):
    name = models.CharField('名前',max_length=255)
    student_number =  models.IntegerField('学籍番号',default=0)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    department = models.ForeignKey(Faculty,on_delete=models.CASCADE)
    year = models.IntegerField('学年',default=0)

    def __str__(self):
        return '<id:' + str(self.id) + ',' + self.name + ',' + self.department + '>'
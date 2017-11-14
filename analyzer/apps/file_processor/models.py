# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time

from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

class Semester(models.Model):
    name = models.CharField(
        null=True, 
        blank=True,
        max_length=10,
        default=""
        )
    number = models.PositiveSmallIntegerField(
        null=True,
        unique=True)
    minimum_credit = models.PositiveSmallIntegerField(
        null=True,
        default=10,
        )
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name
def get_semester():
    return Semester.objects.first() or 0

class Program(models.Model):
    name = models.CharField(max_length=64, blank=True)
    is_full_time = models.BooleanField() # part / full time
    year = models.CharField(max_length=7)
    
    semester_id = models.ForeignKey(Semester, on_delete=models.CASCADE, default=-0)
    def __unicode__(self):
        return self.name
class Course(models.Model):
    name = models.CharField(max_length=64, blank=True)
    code = models.CharField(max_length=64, unique=True)
    semester_id = models.ForeignKey(Semester, on_delete=models.CASCADE)
    # weightage = models.IntegerField(blank=True, null=True)
    program_id = models.ForeignKey(Program, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.name
# def get_user():
#     return User.objects.get(id=1)

class Student(models.Model):
    User = get_user_model()
    name = models.CharField(blank=True, max_length=40) # This is for now!. When every student is a user and there are groups and permissions allotted, name field can be derived from User class
    reg_no = models.CharField(max_length=20)
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=get_user)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name
class Document(models.Model):
    name = models.CharField(max_length=60, blank=True)
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    sha_sum = models.CharField(max_length=256, unique=True)
    # uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.name
    class Meta:
        get_latest_by = "updated_at"

class Exam(models.Model):
    year_string =  time.strftime("%Y, %y")
    year_full, year = year_string.split(",")
    CURRENT_YEAR = year_full + "-" + str(int(year) + 1 )
    
    year = models.CharField(max_length=4, default=CURRENT_YEAR) # In which year exam conducted.
    
    document_id = models.ForeignKey(Document, on_delete=models.CASCADE) # Which document this exam belongs to.
    semester_id = models.ForeignKey(Semester, on_delete=models.CASCADE, default=0)

    is_supplementary_result = models.BooleanField(default=False)
    is_revaluation_result = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        if self.is_revaluation_result or self.is_supplementary_result == False:
            return "Revaluation/Regular"

        return "Supplementary"

class Score(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade = models.CharField(max_length=4, blank=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, default=0)
    
    exam_id = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=True, null=True)
    year = models.CharField(max_length=4, default=Exam.CURRENT_YEAR)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.grade


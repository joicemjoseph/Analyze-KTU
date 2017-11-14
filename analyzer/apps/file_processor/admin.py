# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Program, Course, Student, Score
# Register your models here.
admin.site.register(Program)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Score)
from rest_framework import serializers
from .models import Program, Course, Student, Score

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        exclude = ()
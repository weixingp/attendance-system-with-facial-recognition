from rest_framework import serializers

from main.models import *


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class LabGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabGroup
        fields = '__all__'


class LabSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabSession
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class LabGroupStudentPairSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabGroupStudentPair
        fields = '__all__'


class AttendanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRecord
        fields = '__all__'





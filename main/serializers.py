from drf_yasg import openapi
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


class TakeAttendanceSuccessSerializer(serializers.Serializer):
    success = serializers.BooleanField(help_text="If attendance taking is successful")
    student = StudentSerializer(
        help_text="Display student info if attendance taking is successful",
        required=False
    )
    attendance = AttendanceRecordSerializer(
        help_text="Display the attendance details if attendance taking is successful",
        required=False
    )


class PhotoField(serializers.ImageField):
    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_OBJECT,
            "title": "Photo",
            "properties": {
                "photo": openapi.Schema(
                    title="Photo",
                    type=openapi.TYPE_STRING,
                )
            },
            "required": ["photo"],
        }


class TakeAttendanceWithFaceRecognitionSerializer(serializers.Serializer):
    photo = serializers.ImageField(help_text="Photo containing student's face", label="Photo")


class TakeAttendanceFakeSerializer(serializers.Serializer):
    photo = serializers.CharField(help_text="Photo containing student's face")
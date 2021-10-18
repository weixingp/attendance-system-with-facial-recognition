from django.contrib.auth.models import User
from drf_yasg import openapi
from rest_framework import serializers

from main.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ('is_active', 'id', "date_joined", "last_login")
        extra_kwargs = {
            'password': {'write_only': True},
            'is_superuser': {'help_text': "Determine if the account type is Admin or TA account. Default false (TA Account)"}
        }

        fields = [
            "id",
            "last_login",
            "is_superuser",
            "username",
            "password",
            "email",
            "is_active",
            "date_joined"
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance




class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class LabSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabSession
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class LabGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabGroup
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
        help_text="Display student info",
        required=False
    )
    attendance = AttendanceRecordSerializer(
        help_text="Display the attendance details",
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
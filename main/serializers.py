from rest_framework import serializers

from main.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class LabGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

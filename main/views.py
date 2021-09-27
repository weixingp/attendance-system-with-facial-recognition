from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions

from main.models import Course, LabGroup
from main.serializers import CourseSerializer, LabGroupSerializer
from main.utils.permissions import NonAdminReadOnly


class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows course to be viewed or updated.

    retrieve:
        Return a course instance.

    list:
        Return all courses, ordered by most recently created.

    create:
        Create a new course.

    delete:
        Remove an existing course.

    partial_update:
        Update one or more fields on an existing course.

    update:
        Update a course.
    """
    queryset = Course.objects.all().order_by('-id')
    serializer_class = CourseSerializer
    permission_classes = [NonAdminReadOnly, ]


class LabGroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows lab group to be viewed or updated.
    """
    queryset = LabGroup.objects.all().order_by('-id')
    serializer_class = LabGroupSerializer
    permission_classes = [NonAdminReadOnly, ]
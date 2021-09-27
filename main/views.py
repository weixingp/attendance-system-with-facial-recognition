from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions

from main.models import *
from main.serializers import *
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
    API endpoint that allows Lab Group to be viewed or updated.

    retrieve:
        Return a Lab Group instance.

    list:
        Return all Lab Group, ordered by most recently created.

    create:
        Create a new Lab Group.

    delete:
        Remove an existing Lab Group.

    partial_update:
        Update one or more fields on an existing Lab Group.

    update:
        Update a Lab Group.
    """
    queryset = LabGroup.objects.all().order_by('-id')
    serializer_class = LabGroupSerializer
    permission_classes = [NonAdminReadOnly, ]


class LabSessionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Lab Session to be viewed or updated.

    retrieve:
        Return a Lab Session instance.

    list:
        Return all Lab Sessions, ordered by most recently created.

    create:
        Create a new Lab Session.

    delete:
        Remove an existing Lab Session.

    partial_update:
        Update one or more fields on an existing Lab Session.

    update:
        Update a Lab Session.
    """
    queryset = LabSession.objects.all().order_by('-id')
    serializer_class = LabSessionSerializer
    permission_classes = [NonAdminReadOnly, ]


class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Students to be viewed or updated.

    retrieve:
        Return a Student instance.

    list:
        Return all Students, ordered by most recently created.

    create:
        Create a new Student.

    delete:
        Remove an existing Student.

    partial_update:
        Update one or more fields on an existing Student.

    update:
        Update a Student.
    """
    queryset = Student.objects.all().order_by('-id')
    serializer_class = StudentSerializer
    permission_classes = [NonAdminReadOnly, ]


class AttendanceRecordViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Attendance Records to be viewed or updated.

    retrieve:
        Return a Attendance Record instance.

    list:
        Return all Attendance Records, ordered by most recently created.

    create:
        Create a new Attendance Record.

    delete:
        Remove an existing Attendance Record.

    partial_update:
        Update one or more fields on an existing Attendance Record.

    update:
        Update a Attendance Record.
    """
    queryset = AttendanceRecord.objects.all().order_by('-id')
    serializer_class = AttendanceRecordSerializer
    permission_classes = [NonAdminReadOnly, ]


class LabGroupStudentPairViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Lab Group Student Pairs to be viewed or updated.

    retrieve:
        Return a Lab Group Student Pair instance.

    list:
        Return all Lab Group Student Pair, ordered by most recently created.

    create:
        Create a new Lab Group Student Pair.

    delete:
        Remove an existing Lab Group Student Pair.

    partial_update:
        Update one or more fields on an existing Lab Group Student Pair.

    update:
        Update a Lab Group Student Pair.
    """
    queryset = LabGroupStudentPair.objects.all().order_by('-id')
    serializer_class = LabGroupStudentPairSerializer
    permission_classes = [NonAdminReadOnly, ]
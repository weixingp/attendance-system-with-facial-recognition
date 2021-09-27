from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
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


# class StudentsInGroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows students in a specific Lab Group to be viewed or updated.
#
#     retrieve:
#         Return a Student Lab Group Pair instance.
#
#     list:
#         Return all students in Lab Group, ordered by most recently created.
#
#     create:
#         Create a new student Lab Group Pair .
#
#     delete:
#         Remove an existing Lab Group Student Pair.
#
#     partial_update:
#         Update one or more fields on an existing Lab Group Student Pair.
#
#     update:
#         Update a Lab Group Student Pair.
#     """
#
#     serializer_class = LabGroupStudentPairSerializer
#     permission_classes = [NonAdminReadOnly, ]
#
#     def get_queryset(self):
#         group_id = self.kwargs['group_id']
#         queryset = LabGroupStudentPair.objects.filter(group_id=group_id).order_by('-id')
#         return queryset
#
#     # @staticmethod
#     # def get_students_in_lab_group(pk):
#     #     try:
#     #         return LabGroupStudentPair.objects.get(pk=pk)
#     #     except LabGroupStudentPair.DoesNotExist:
#     #         raise Http404
#
#     # def get(self, request, pk):
#     #     students_in_lab_group = self.get_students_in_lab_group(pk)
#     #
#     # @action(methods=['get'], detail=True)
#     # def studentlist(self, request, pk=group_id):
#     #     try:
#     #         student_in_lab_group = LabGroupStudentPair.objects.get('lab_group' == pk)
#     #     except student_in_lab_group.DoesNotExist:
#     #         return Response({"error": "Lab Group not found."},
#     #                         status=status.HTTP_400_BAD_REQUEST)
#     #     studentlist = student_in_lab_group.objects.distinct('student')
#     #     return Response(LabGroupStudentPairSerializer(studentlist, many=True))

from django.core.cache import cache
from django.db import transaction
from django.http import Http404
from django.shortcuts import render

# Create your views here.
from django.utils.timezone import localtime
from drf_yasg.openapi import Schema
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from attendance_taking_webapp.settings import DEFAULT_CACHE_TIME
from main.models import *
from main.serializers import *
from main.utils.FaceRecognition import FaceRecognitionManager
from main.utils.permissions import NonAdminReadOnly


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user to be viewed or updated.

    retrieve:
        Return a user instance.

    list:
        Return all users, ordered by most recently created.

    create:
        Create a new user.

    delete:
        Remove an existing user.

    partial_update:
        Update one or more fields on an existing user.

    update:
        Update a user.
    """
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, ]


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
    parser_classes = (MultiPartParser,)
    filterset_fields = ('matric', )

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        student = serializer.save()
        verified = FaceRecognitionManager.check_photo(student.photo)

        if not verified:
            err = ValidationError(detail="No face detected in student photo")
            err.status_code = 500
            raise err

    @transaction.atomic
    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        student = serializer.save()
        verified = FaceRecognitionManager.check_photo(student.photo)

        if not verified:
            err = ValidationError(detail="No face detected in student photo")
            err.status_code = 500
            raise err

        student.delete_face_recognition_cache()

    def perform_destroy(self, instance):
        instance.delete_face_recognition_cache()
        super(StudentViewSet, self).perform_destroy(instance)


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
    filterset_fields = ('lab_session',)


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
    filterset_fields = ('student__matric', 'lab_group__id', )

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        student_in_lab_grp = serializer.save()
        student_in_lab_grp.student.delete_face_recognition_cache()

    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        student_in_lab_grp = serializer.save()
        student_in_lab_grp.student.delete_face_recognition_cache()

    def perform_destroy(self, instance):
        instance.student.delete_face_recognition_cache()
        super(LabGroupStudentPairViewSet, self).perform_destroy(instance)

    # def list(self, request, *args, **kwargs):
    #     # do your customization here
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(many=True)
    #     print(serializer.data)
    #     data = serializer.data
    #     for item in data:
    #         print(item)
    #         student = Student.objects.get(pk=item["student"])
    #         item["student"] = StudentSerializer(student).data
    #     return Response(data)


class TakeAttendanceWithFaceRecognitionView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TakeAttendanceWithFaceRecognitionSerializer
    parser_classes = (MultiPartParser,)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            # queryset just for schema generation metadata
            return LabSession.objects.none()

    @staticmethod
    def get_session(pk):
        try:
            return LabSession.objects.get(pk=pk)
        except LabSession.DoesNotExist:
            raise Http404

    # def get_serializer(self):
    #     return self.serializer_class
    #
    # def get_queryset(self):
    #     if getattr(self, 'swagger_fake_view', False):
    #         # queryset just for schema generation metadata
    #         return LabSession.objects.none()

    @swagger_auto_schema(
        responses={200: TakeAttendanceSuccessSerializer()},
    )
    @transaction.atomic
    def post(self, request, pk):
        """
        API endpoint that allows attendance to be submitted with photo of student's face
        """
        session = self.get_session(pk)
        lab_grp = session.lab_group

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        photo = serializer.validated_data["photo"]

        cache_key = f"session_id_{session.id}"
        cache_value = cache.get(cache_key)
        if cache_value is not None:
            manager = cache_value
        else:
            manager = FaceRecognitionManager(lab_group=lab_grp)
            cache.set(cache_key, manager, DEFAULT_CACHE_TIME)

        result = manager.recognise_student(photo=photo)
        if result:
            # Todo: Add attendance record if successful

            attendance_record = AttendanceRecord.objects.filter(student=result, lab_session=session)
            if not attendance_record:
                attendance = AttendanceRecord.objects.create(
                    student=result,
                    lab_session=session,
                    status="1",
                    is_taken_with_facial_recognition=True,
                    date_time_captured=localtime()
                )

                data = {
                    "success": True,
                    "student": StudentSerializer(result).data,
                    "attendance": AttendanceRecordSerializer(attendance).data
                }
            else:
                err = ValidationError(detail="Attendance for this student has already been recorded for this lab session.")
                err.status_code = 500
                raise err
        else:
            err = ValidationError(detail="Unable to identify the student, perhaps the student is not in this lab group.")
            err.status_code = 500
            raise err

        s = TakeAttendanceSuccessSerializer(data=data)
        s.is_valid(raise_exception=False)
        res = s.data
        return Response(res)

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

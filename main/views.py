from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions

from main.models import Course, LabGroup
from main.serializers import CourseSerializer, LabGroupSerializer
from main.utils.permissions import NonAdminReadOnly


class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows course to be viewed or updated.
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
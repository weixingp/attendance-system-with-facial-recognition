import random
import string
from urllib import parse

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User, Group
from django.db import models
from django.db.models import CharField
from django.forms import forms
from django.utils.safestring import mark_safe
from main.validators import validate_matric
from django.utils.translation import ugettext_lazy as _


# Create your models here.


class Course(models.Model):
    """
    Represents a Course that Students registered for. Related to :model:`Lab Group`.
    """
    courseCode = models.CharField(max_length=64)  # need to set unique
    course_name = models.CharField(max_length=64)

    def __str__(self):
        return self.courseCode


class LabGroup(models.Model):
    """
    Represents a Lab Group belonging to a specific Course. Related to :model:'Course`.
    """
    courseGroup = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_lab_group")
    labGroupName = models.CharField(max_length=64)

    # Object name for display in admin panel
    def __str__(self):
        return "%s - %s" % (self.labGroupName, self.courseGroup.courseCode)


class LabSession(models.Model):
    """
    Represents a Lab Session belonging to a specific Lab Group. Related to :model:'Lab Group`.
    """
    sessionName = models.CharField(max_length=64)
    labGroup = models.ForeignKey(LabGroup, on_delete=models.CASCADE, related_name="lab_group_session")
    dateTimeStart = models.DateTimeField(null=False, auto_now=False)
    dateTimeEnd = models.DateTimeField(null=False, auto_now=False)

    # Object name for display in admin panel
    def __str__(self):
        return "%s - %s" % (self.sessionName, self.labGroup.labGroupName)


class Student(models.Model):
    """
    Represents a student. Related to :model:'Lab Group`.
    """
    studentName = models.CharField(max_length=64)
    studentMatric = models.CharField(max_length=9, unique=True)
    labGroup = models.ForeignKey(LabGroup, on_delete=models.CASCADE, related_name="student_lab_group")
    photoUploaded = models.BooleanField(default=False)

    # Object name for display in admin panel
    def __str__(self):
        return self.studentName + " - " + self.studentMatric


class attendanceRecord(models.Model):
    """
    Represents a student's attendance for a specific lab session. Related to :model:`student`, :model:`labSession`.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="student_attendance")
    labSession = models.ForeignKey(LabSession, on_delete=models.CASCADE, related_name="student_lab_session")
    ATTENDANCE_STATUS = (
        "Absent",
        "Present",
        "Late",
    )
    status = models.CharField(
        max_length=1,
        choices=ATTENDANCE_STATUS,
        help_text="Absent, Present, Late"
    )
    dateTime_captured = models.DateTimeField(null=True)
    dateTime_modified = models.DateTimeField(auto_now=True)
    remarks = models.CharField(max_length=128)

    def __str__(self):
        return "%s | %s | %s" % (self.student.studentMatric, self.labSession.labGroup, self.status)


class AccountProfile(models.Model):
    """
    Represents a account's profile. Related to :model:`auth.User` and :model:`main.Class`.
    """
    account_User = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    privilege_level = (
        "Admin",
        "Course Coord",
        "TA",
    )
    status = models.CharField(
        max_length=1,
        choices=privilege_level,
        help_text="Admin, Course Coord, TA"
    )
    userName = models.CharField(max_length=64, null=False, unique=True)
    email = models.CharField(max_length=64, null=False, unique=True)
    has_reset_password = models.BooleanField(default=False)

    def __str__(self):
        return self.email + " : " + self.userName + " (" + self.status + ")"


from django.db import models


# Create your models here.
from main.utils.custom_fields import ContentTypeRestrictedFileField


class Course(models.Model):
    """
    Represents a Course that Students registered for. Related to :model:`Lab Group`.
    """
    course_code = models.CharField(max_length=128, unique=True)  # need to set unique
    course_name = models.CharField(max_length=128)

    def __str__(self):
        return self.course_code


class LabGroup(models.Model):
    """
    Represents a Lab Group belonging to a specific Course. Related to :model:'Course`.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lab_group_name = models.CharField(max_length=64)

    # Object name for display in admin panel
    def __str__(self):
        return "%s - %s" % (self.lab_group_name, self.course.course_code)


class LabSession(models.Model):
    """
    Represents a Lab Session belonging to a specific Lab Group. Related to :model:'Lab Group`.
    """
    session_name = models.CharField(max_length=64)
    lab_group = models.ForeignKey(LabGroup, on_delete=models.CASCADE)
    date_time_start = models.DateTimeField(null=False, auto_now=False)
    date_time_end = models.DateTimeField(null=False, auto_now=False)

    # Object name for display in admin panel
    def __str__(self):
        return "%s - %s" % (self.session_name, self.lab_group.lab_group_name)


class Student(models.Model):
    """
    Represents a student. Related to :model:'Lab Group`.
    """
    name = models.CharField(max_length=64)
    matric = models.CharField(max_length=9, unique=True)
    lab_group = models.ForeignKey(LabGroup, on_delete=models.CASCADE)
    photo = ContentTypeRestrictedFileField(
        upload_to=ContentTypeRestrictedFileField.update_student_photo_filename,
        content_types=['image/jpg', 'image/png', 'image/gif'],
        max_upload_size=1500000,
        null=True,
        blank=True,
    )

    # Object name for display in admin panel
    def __str__(self):
        return self.name + " - " + self.matric


class AttendanceRecord(models.Model):
    """
    Represents a student's attendance for a specific lab session. Related to :model:`student`, :model:`labSession`.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lab_session = models.ForeignKey(LabSession, on_delete=models.CASCADE)
    ATTENDANCE_STATUS = (
        ("1", "Present"),
        ("2", "Absent"),
        ("3", "Late"),
        ("4", "Absent with valid reason"),
    )

    status = models.CharField(
        max_length=1,
        choices=ATTENDANCE_STATUS,
        help_text="Attendance status"
    )
    date_time_captured = models.DateTimeField(null=True)
    date_time_modified = models.DateTimeField(auto_now=True)
    remarks = models.CharField(max_length=256)

    def __str__(self):
        return "%s | %s | %s" % (self.student.matric, self.lab_session.lab_group, self.status)


# class AccountProfile(models.Model):
#     """
#     Represents a account's profile. Related to :model:`auth.User` and :model:`main.Class`.
#     """
#     account_User = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
#     privilege_level = (
#         "Admin",
#         "Course Coord",
#         "TA",
#     )
#     status = models.CharField(
#         max_length=1,
#         choices=privilege_level,
#         help_text="Admin, Course Coord, TA"
#     )
#     userName = models.CharField(max_length=64, null=False, unique=True)
#     email = models.CharField(max_length=64, null=False, unique=True)
#     has_reset_password = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.email + " : " + self.userName + " (" + self.status + ")"


# Generated by Django 3.2.7 on 2021-09-27 11:50

from django.db import migrations
import main.utils.custom_fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_labgroupstudentpair'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='photo',
            field=main.utils.custom_fields.ContentTypeRestrictedFileField(upload_to=main.utils.custom_fields.ContentTypeRestrictedFileField.update_student_photo_filename),
        ),
    ]
# Generated by Django 2.2.2 on 2020-05-18 00:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0012_auto_20200518_0112'),
    ]

    operations = [
        migrations.RenameField(
            model_name='school',
            old_name='student_view_student_details',
            new_name='student_can_view_student_details',
        ),
        migrations.RenameField(
            model_name='school',
            old_name='teacher_view_student_details',
            new_name='teacher_can_view_student_details',
        ),
    ]

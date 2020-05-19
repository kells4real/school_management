
from django.urls import path
from .views import (admin_page, student_register,
    admin_register, student_list, student_jss1,
    student_jss2, student_jss3, student_ss1, student_ss2,
                    student_ss3, edit_student,
                    teacher_list, teacher_register,
                    edit_teacher, DeleteStudent, DeleteTeacher,
                    admin_settings)

urlpatterns = [
    path('', admin_page, name="admin-page"),
    path('students_list/jss1/', student_jss1, name='student-jss1'),
    path('students_list/jss2/', student_jss2, name='student-jss2'),
    path('students_list/jss3/', student_jss3, name='student-jss3'),
    path('students_list/ss1/', student_ss1, name='student-ss1'),
    path('students_list/ss2/', student_ss2, name='student-ss2'),
    path('students_list/ss3/', student_ss3, name='student-ss3'),
    path('students_list/', student_list, name='student-list'),
    path('register/student/', student_register, name="student-register"),
    path('register/admin/', admin_register, name="admin-register"),
    path('register/teacher/', teacher_register, name="teacher-register"),
    path('edit_student/<int:pk>/', edit_student, name="edit-student"),
    path('edit_teacher/<int:pk>/', edit_teacher, name="edit-teacher"),
    path('teachers_list/', teacher_list, name="teacher-list"),
    path('teacher_delete/', DeleteTeacher.as_view(), name="teacher-delete"),
    path('student_delete/', DeleteStudent.as_view(), name='student-delete'),
    path('settings/', admin_settings, name="admin-settings"),
]
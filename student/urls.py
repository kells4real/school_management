
from django.urls import path
from .views import student, single_student

urlpatterns = [
    path('', student, name="student"),
    path('<slug>/', single_student, name='single-student'),
    # path('registration/', views.student_regi, name='student_regi'),
]
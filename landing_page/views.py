from django.shortcuts import render
from management.models import User, School
# Create your views here.


def home(request):
    teachers = User.objects.filter(is_teacher=True).count()
    students = User.objects.filter(is_student=True).count()
    schools = School.objects.all().count()
    users = User.objects.all().count()

    return render(request, 'landing_page/index.html',
                  {"teachers": teachers, "students": students, "schools": schools,
                   "users": users})


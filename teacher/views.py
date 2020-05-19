from django.shortcuts import render, get_object_or_404
from management.models import TeacherProfile
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required
from management.models import Class

# Create your views here.

def student(request):
    return render(request, 'student/student.html')

@login_required
def single_teacher(request, slug):
    teacher_single = get_object_or_404(TeacherProfile, slug=slug)
    subjects = teacher_single.user.subject.all
    classes = teacher_single.user.classes.all
    salary = teacher_single.user.salary

    jss1 = Class.objects.get(name="JSS 1")
    jss2 = Class.objects.get(name="JSS 2")
    jss3 = Class.objects.get(name="JSS 3")
    ss1 = Class.objects.get(name="SS 1")
    ss2 = Class.objects.get(name="SS 2")
    ss3 = Class.objects.get(name="SS 3")

    if request.user == teacher_single.user or request.user.is_admin and request.user.school == teacher_single.user.school:
        context = {
            "single_teacher": teacher_single,
            'object': teacher_single.user,

            'subjects': subjects,
            'salary': salary,
            'classes': classes,
            'jss1': jss1,
            'jss2': jss2,
            'jss3': jss3,
            'ss1': ss1,
            'ss2': ss2,
            'ss3': ss3
        }
        return render(request, "teacher/teacher_details.html", context)
    # else:
    #     return render(request, "student/student_details.html")

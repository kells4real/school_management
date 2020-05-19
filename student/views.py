from django.shortcuts import render, get_object_or_404
from management.models import StudentProfile, Class
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.

def student(request):
    return render(request, 'student/student.html')

@login_required
def single_student(request, slug):
    student_single = get_object_or_404(StudentProfile, slug=slug)

    if request.user == student_single.user or (request.user.is_teacher and request.user.school == student_single.user.school) or (request.user.is_admin and request.user.school == student_single.user.school):
        class_get = request.user.student_class
        jss1 = Class.objects.get(name="JSS 1")
        jss2 = Class.objects.get(name="JSS 2")
        jss3 = Class.objects.get(name="JSS 3")
        ss1 = Class.objects.get(name="SS 1")
        ss2 = Class.objects.get(name="SS 2")
        ss3 = Class.objects.get(name="SS 3")
        context = {
            "single_student": student_single,
            'object': student_single.user,
            "class": class_get,
        'jss1': jss1,
        'jss2': jss2,
        'jss3': jss3,
        'ss1': ss1,
        'ss2': ss2,
        'ss3': ss3,
        }
        return render(request, "student/student_details.html", context)
    # else:
    #     return render(request, "student/student_details.html")


# def edit_student(request, pk):
#     student_edit = StudentProfile.objects.get(id=pk)
#     edit_forms = CreateStudent(instance=student_edit)
#
#     if request.method == "POST":
#         edit_forms = CreateStudent(request.POST, instance=student_edit)
#
#         if edit_forms.is_valid():
#             edit_forms.save()
#             messages.success(request, "Edit Student Info Successfully!")
#             return redirect("student_list")
#
#     context = {
#         "edit_forms": edit_forms
#     }
#     return render(request, "students/edit_student.html", context)
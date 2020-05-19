from django.shortcuts import render, redirect, get_object_or_404, reverse
from .forms import (StudentRegisterForm,
                    AdminRegisterForm,
                    TeacherRegisterForm,
                    UpdateStudentRegisterForm,
                    UpdateTeacherRegisterForm,
                    SettingsForm)
import sweetify
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from .tokens import account_activation_token
from .models import RegistrationLinks
from management.models import User, StudentProfile, TeacherProfile, Class, School
from .models import Defaulters

from django.contrib.auth import login, logout
from django.conf import settings
from django.views.generic import DeleteView, View
from django.urls import reverse_lazy



def admin_page(request):
    obj = request.user

    return render(request, 'admin_/home.html', {"object": obj })


def student_register(request):
    meta_tags = ["free web page", "sign up", "free SEO", 'free publicity', "free web optimization", "free advertising",
                 "fashion", "style", "african", "africa", "african fashion", "free SMO"]
    meta_title = "African Fashion | Sign-up"
    meta_description = "Join the growing community, get free publicity, search engine optimization and more."
    meta_url = request.build_absolute_uri()
    active = "signup"
    if request.method == 'POST':
        register_form = StudentRegisterForm(request.POST, request.FILES)

        word_list = ["admin", "admin-account", "admin_account", "porn", "fuck", "bitch", "ass-hole", "asshole", "nigga",
             "bitch-ass", "vigina", "penis", "dick-head", "register"]

        if register_form.is_valid():
            user = register_form.save(commit=False)
            if user.username in word_list:
                sweetify.sweetalert(request, "Info", text=f"Username {user.username} not accepted on this site, please choose another.",
                                    icon="info", persistent=True)
                return redirect('register')

            else:
                user.email = register_form.cleaned_data['email']
                user.set_password(register_form.cleaned_data['password'])
                # user.is_active = False
                # Assign student privileges to the user
                user.is_student = True
                user.school = request.user.school
                user.save()
                sweetify.sweetalert(request, "Success!", text="Student Created", icon="success")
                # meta_tags = ["free web page", "sign up", "free seo", 'free publicity', "free web optimization", "free advertising", "fashion", "style", "african", "africa", "african fashion"]
                # current_site = get_current_site(request)
                # subject = 'Activate your Account'
                # # create Message
                # uid = urlsafe_base64_encode(force_bytes(user.pk))
                # token = account_activation_token.make_token(user)
                # built_link = f"https://{request.get_host()}/activate/{uid}/{token}/"
                # message = render_to_string('admin_/welcome_email.html', {
                #     'user': user,
                #     'domain': current_site.domain,
                #     'uid': uid,
                #     'token': token,
                # })
                # # send activation link to the user
                #
                # user.email_user(subject=subject, message=message)
                #
                # sweetify.sweetalert(request, ' Account has been created successfully, '
                #                           ' the owner still has to check his/her mail for a link '
                #                           'to activate the account before they can sign in. '
                #                              'Mails may sometimes go to spam,  or you may click resend link at '
                #                              'login page to request for the link again..',
                #                     persistent="OK")
                #
                # save_link = RegistrationLinks.objects.create(user=user, link=built_link, email=user.email)
                # save_link.save()

                return redirect('admin-page')

    else:
        register_form = StudentRegisterForm()

    return render(request, 'admin_/student_registration.html', {'form': register_form, 'meta_tags':meta_tags , "meta_title": meta_title, "meta_url":meta_url, "active":active,
                                                   "meta_description": meta_description, 'GOOGLE_RECAPTCHA_SITE_KEY': settings.GOOGLE_RECAPTCHA_SITE_KEY, "object": request.user })


def activate_link(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid) # Get the user with that uid
    except(TypeError, ValueError, OverflowError,User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        logout(request) # if parameters are met, then logout any user on the browser to allow for log in
        user.is_active = True # update user status to active
        user.save()
        # login(request, user)
        sweetify.sweetalert(request, "Success!", text="Email verification successful. You may now sign in.", icon="success")
        return redirect('login')
    else:
        return render(request, 'admin_/account_activation_invalid.html')


def admin_register(request):
    if request.user.is_superuser:
        meta_tags = ["free web page", "sign up", "free SEO", 'free publicity', "free web optimization", "free advertising",
                     "fashion", "style", "african", "africa", "african fashion", "free SMO"]
        meta_title = "African Fashion | Sign-up"
        meta_description = "Join the growing community, get free publicity, search engine optimization and more."
        meta_url = request.build_absolute_uri()
        active = "signup"
        if request.method == 'POST':
            register_form = AdminRegisterForm(request.POST, request.FILES)

            word_list = ["admin", "admin-account", "admin_account", "porn", "fuck", "bitch", "ass-hole", "asshole", "nigga",
                 "bitch-ass", "vigina", "penis", "dick-head", "register"]

            if register_form.is_valid():
                user = register_form.save(commit=False)
                if user.username in word_list:
                    sweetify.sweetalert(request, "Info", text=f"Username {user.username} not accepted on this site, please choose another.",
                                        icon="info", persistent=True)
                    return redirect('register')

                else:
                    user.email = register_form.cleaned_data['email']
                    user.set_password(register_form.cleaned_data['password'])
                    # user.is_active = False
                    # Assign student privileges to the user
                    user.is_admin = True
                    user.save()
                    sweetify.sweetalert(request, "Success!", text="Student Created", icon="success")
                    # meta_tags = ["free web page", "sign up", "free seo", 'free publicity', "free web optimization", "free advertising", "fashion", "style", "african", "africa", "african fashion"]
                    # current_site = get_current_site(request)
                    # subject = 'Activate your Account'
                    # # create Message
                    # uid = urlsafe_base64_encode(force_bytes(user.pk))
                    # token = account_activation_token.make_token(user)
                    # built_link = f"https://{request.get_host()}/activate/{uid}/{token}/"
                    # message = render_to_string('admin_/welcome_email.html', {
                    #     'user': user,
                    #     'domain': current_site.domain,
                    #     'uid': uid,
                    #     'token': token,
                    # })
                    # # send activation link to the user
                    #
                    # user.email_user(subject=subject, message=message)
                    #
                    # sweetify.sweetalert(request, ' Account has been created successfully, '
                    #                           ' the owner still has to check his/her mail for a link '
                    #                           'to activate the account before they can sign in. '
                    #                              'Mails may sometimes go to spam,  or you may click resend link at '
                    #                              'login page to request for the link again..',
                    #                     persistent="OK")
                    #
                    # save_link = RegistrationLinks.objects.create(user=user, link=built_link, email=user.email)
                    # save_link.save()

                    return redirect('home-login')

        else:
            register_form = AdminRegisterForm()

        return render(request, 'admin_/admin_register.html', {'form': register_form, 'meta_tags':meta_tags , "meta_title": meta_title, "meta_url":meta_url, "active":active,
                                                       "meta_description": meta_description, 'GOOGLE_RECAPTCHA_SITE_KEY': settings.GOOGLE_RECAPTCHA_SITE_KEY, })
    else:
        return redirect("home-login")


def teacher_register(request):
    meta_tags = ["free web page", "sign up", "free SEO", 'free publicity', "free web optimization", "free advertising",
                 "fashion", "style", "african", "africa", "african fashion", "free SMO"]
    meta_title = "African Fashion | Sign-up"
    meta_description = "Join the growing community, get free publicity, search engine optimization and more."
    meta_url = request.build_absolute_uri()
    active = "signup"
    if request.method == 'POST':
        form = TeacherRegisterForm(request.POST, request.FILES)

        word_list = ["admin", "admin-account", "admin_account", "porn", "fuck", "bitch", "ass-hole", "asshole", "nigga",
             "bitch-ass", "vigina", "penis", "dick-head", "register"]

        if form.is_valid():
            user = form.save(commit=False)
            if user.username in word_list:
                sweetify.sweetalert(request, "Info", text=f"Username {user.username} not accepted on this site, please choose another.",
                                    icon="info", persistent=True)
                return redirect('register')

            else:
                user.email = form.cleaned_data['email']
                user.set_password(form.cleaned_data['password'])
                # user.is_active = False
                # Assign student privileges to the user
                user.is_teacher = True
                user.school = request.user.school
                user.save()
                form.save_m2m()
                sweetify.sweetalert(request, "Success!", text="Teacher Created", icon="success")
                # meta_tags = ["free web page", "sign up", "free seo", 'free publicity', "free web optimization", "free advertising", "fashion", "style", "african", "africa", "african fashion"]
                # current_site = get_current_site(request)
                # subject = 'Activate your Account'
                # # create Message
                # uid = urlsafe_base64_encode(force_bytes(user.pk))
                # token = account_activation_token.make_token(user)
                # built_link = f"https://{request.get_host()}/activate/{uid}/{token}/"
                # message = render_to_string('admin_/welcome_email.html', {
                #     'user': user,
                #     'domain': current_site.domain,
                #     'uid': uid,
                #     'token': token,
                # })
                # # send activation link to the user
                #
                # user.email_user(subject=subject, message=message)
                #
                # sweetify.sweetalert(request, ' Account has been created successfully, '
                #                           ' the owner still has to check his/her mail for a link '
                #                           'to activate the account before they can sign in. '
                #                              'Mails may sometimes go to spam,  or you may click resend link at '
                #                              'login page to request for the link again..',
                #                     persistent="OK")
                #
                # save_link = RegistrationLinks.objects.create(user=user, link=built_link, email=user.email)
                # save_link.save()

                return redirect('admin-page')

    else:
        form = TeacherRegisterForm()

    return render(request, 'admin_/create_teacher.html', {'form': form, 'meta_tags':meta_tags , "meta_title": meta_title, "meta_url":meta_url, "active":active,
                                                   "meta_description": meta_description, 'GOOGLE_RECAPTCHA_SITE_KEY': settings.GOOGLE_RECAPTCHA_SITE_KEY, })


def student_list(request):
    students = User.objects.filter(is_student=True, school=request.user.school).order_by('date_joined')
    paginator = Paginator(students, 1)
    page_number = request.GET.get('page')
    try:
        page_objects = paginator.page(page_number)
    except PageNotAnInteger:
        page_objects = paginator.page(1)
    except EmptyPage:
        page_objects = paginator.page(paginator.num_pages)

    context = {
        "students": page_objects,
        'object': request.user
    }
    return render(request, "student/student_list.html", context)


def teacher_list(request):
    teachers = User.objects.filter(is_teacher=True, school=request.user.school).order_by('date_joined')

    paginator = Paginator(teachers, 1)
    page_number = request.GET.get('page')
    try:
        page_objects = paginator.page(page_number)
    except PageNotAnInteger:
        page_objects = paginator.page(1)
    except EmptyPage:
        page_objects = paginator.page(paginator.num_pages)

    context = {
        "teachers": page_objects
    }
    return render(request, "teacher/teacher_list.html", context)


def edit_student(request, pk):
    student = User.objects.get(id=pk)
    if request.method == "POST":
        form = UpdateStudentRegisterForm(request.POST, request.FILES, instance=student)

        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            sweetify.sweetalert(request, "Success!",  text="Student info updated", icon="success")
            return redirect("student-list")

    else:
        form = UpdateStudentRegisterForm(instance=student)
    context = {
        "form": form
    }
    return render(request, "admin_/edit_student.html", context)


def edit_teacher(request, pk):
    teacher = User.objects.get(id=pk)
    if request.method == "POST":
        form = UpdateTeacherRegisterForm(request.POST, request.FILES, instance=teacher)

        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            form.save_m2m()
            sweetify.sweetalert(request, "Success!",  text="Teacher info updated", icon="success")
            return redirect("teacher-list")

    else:
        form = UpdateTeacherRegisterForm(instance=teacher)
    context = {
        "form": form
    }
    return render(request, "admin_/edit_teacher.html", context)

from django.http import JsonResponse

# def delete_teacher(request, pk):
#     teacher = User.objects.get(pk=pk)
#     data = dict()
#     # teacher_delete.delete()
#     # sweetify.sweetalert(request,"Success!",  text="Teacher Deleted", icon="success")
#     # return redirect("teacher-list")
#
#     if request.method == 'POST':
#         teacher.delete()
#         # data['form_is_valid'] = True  # This is just to play along with the existing code
#         # teachers = User.objects.filter(is_teacher=True, school=request.user.school)
#         # data['html_book_list'] = render_to_string('teacher/teacher_list.html', {
#         #     'teachers': teachers
#         # })
#     else:
#         context = {'teacher': teacher}
#         data['html_form'] = render_to_string('admin_/delete_modal.html',
#             context,
#             request=request,
#         )
#     return JsonResponse(data)


class DeleteStudent(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        usr = User.objects.get(id=id1)
        if self.request.user.is_admin and usr.school == self.request.user.school:
            User.objects.get(id=id1).delete()
            data = {
                'deleted': True
            }
            return JsonResponse(data)


class DeleteTeacher(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        usr = User.objects.get(id=id1)
        if self.request.user.is_admin and usr.school == self.request.user.school:
            User.objects.get(id=id1).delete()
            data = {
                'deleted': True
            }
            return JsonResponse(data)


# class TeacherDelete(DeleteView):
#     model = User
#     template_name = 'admin_/delete_modal.html'
#
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     context.update({
#     #         "delete": "Message",
#     #         "active" : "messages"
#     #     })
#     #
#     #     return context
#
#     def test_func(self):
#         teacher = self.get_object()
#         if self.request.user.is_admin and self.request.user.school == teacher.school:
#             return True
#         return False
#
#     def get_success_url(self):
#         sweetify.success(self.request, "Teacher Deleted")
#         return reverse_lazy('teacher-list')


def student_jss1(request):
    class_ = Class.objects.get(name="JSS 1")
    students = User.objects.filter(is_student=True, school=request.user.school, student_class=class_).order_by('date_joined')
    paginator = Paginator(students, 1)
    page_number = request.GET.get('page')
    try:
        page_objects = paginator.page(page_number)
    except PageNotAnInteger:
        page_objects = paginator.page(1)
    except EmptyPage:
        page_objects = paginator.page(paginator.num_pages)

    jss1 = Class.objects.get(name="JSS 1")
    jss2 = Class.objects.get(name="JSS 2")
    jss3 = Class.objects.get(name="JSS 3")
    ss1 = Class.objects.get(name="SS 1")
    ss2 = Class.objects.get(name="SS 2")
    ss3 = Class.objects.get(name="SS 3")

    classes = request.user.classes.all

    class_get = request.user.student_class

    context = {
        "students": page_objects,
        'object': request.user,
        'classes': classes,
        'jss1': jss1,
        'jss2': jss2,
        'jss3': jss3,
        'ss1': ss1,
        'ss2': ss2,
        'ss3': ss3,
        "class": class_get
    }
    return render(request, "student/student_list.html", context)


def student_jss2(request):
    class_ = Class.objects.get(name="JSS 2")
    students = User.objects.filter(is_student=True, school=request.user.school, student_class=class_).order_by('date_joined')
    paginator = Paginator(students, 1)
    page_number = request.GET.get('page')
    try:
        page_objects = paginator.page(page_number)
    except PageNotAnInteger:
        page_objects = paginator.page(1)
    except EmptyPage:
        page_objects = paginator.page(paginator.num_pages)

    jss1 = Class.objects.get(name="JSS 1")
    jss2 = Class.objects.get(name="JSS 2")
    jss3 = Class.objects.get(name="JSS 3")
    ss1 = Class.objects.get(name="SS 1")
    ss2 = Class.objects.get(name="SS 2")
    ss3 = Class.objects.get(name="SS 3")

    classes = request.user.classes.all

    class_get = request.user.student_class

    context = {
        "students": page_objects,
        'object': request.user,
        'classes': classes,
        'jss1': jss1,
        'jss2': jss2,
        'jss3': jss3,
        'ss1': ss1,
        'ss2': ss2,
        'ss3': ss3,
        "class": class_get
    }
    return render(request, "student/student_list.html", context)


def student_jss3(request):
    class_ = Class.objects.get(name="JSS 3")
    students = User.objects.filter(is_student=True, school=request.user.school, student_class=class_).order_by('date_joined')
    paginator = Paginator(students, 1)
    page_number = request.GET.get('page')
    try:
        page_objects = paginator.page(page_number)
    except PageNotAnInteger:
        page_objects = paginator.page(1)
    except EmptyPage:
        page_objects = paginator.page(paginator.num_pages)

    jss1 = Class.objects.get(name="JSS 1")
    jss2 = Class.objects.get(name="JSS 2")
    jss3 = Class.objects.get(name="JSS 3")
    ss1 = Class.objects.get(name="SS 1")
    ss2 = Class.objects.get(name="SS 2")
    ss3 = Class.objects.get(name="SS 3")

    classes = request.user.classes.all

    class_get = request.user.student_class

    context = {
        "students": page_objects,
        'object': request.user,
        'classes': classes,
        'jss1': jss1,
        'jss2': jss2,
        'jss3': jss3,
        'ss1': ss1,
        'ss2': ss2,
        'ss3': ss3,
        "class": class_get
    }
    return render(request, "student/student_list.html", context)


def student_ss1(request):
    class_ = Class.objects.get(name="SS 1")
    students = User.objects.filter(is_student=True, school=request.user.school, student_class=class_).order_by('date_joined')
    paginator = Paginator(students, 1)
    page_number = request.GET.get('page')
    try:
        page_objects = paginator.page(page_number)
    except PageNotAnInteger:
        page_objects = paginator.page(1)
    except EmptyPage:
        page_objects = paginator.page(paginator.num_pages)

    jss1 = Class.objects.get(name="JSS 1")
    jss2 = Class.objects.get(name="JSS 2")
    jss3 = Class.objects.get(name="JSS 3")
    ss1 = Class.objects.get(name="SS 1")
    ss2 = Class.objects.get(name="SS 2")
    ss3 = Class.objects.get(name="SS 3")

    classes = request.user.classes.all

    class_get = request.user.student_class

    context = {
        "students": page_objects,
        'object': request.user,
        'classes': classes,
        'jss1': jss1,
        'jss2': jss2,
        'jss3': jss3,
        'ss1': ss1,
        'ss2': ss2,
        'ss3': ss3,
        "class": class_get
    }
    return render(request, "student/student_list.html", context)


def student_ss2(request):
    class_ = Class.objects.get(name="SS 2")
    students = User.objects.filter(is_student=True, school=request.user.school, student_class=class_).order_by('date_joined')
    paginator = Paginator(students, 1)
    page_number = request.GET.get('page')
    try:
        page_objects = paginator.page(page_number)
    except PageNotAnInteger:
        page_objects = paginator.page(1)
    except EmptyPage:
        page_objects = paginator.page(paginator.num_pages)

    jss1 = Class.objects.get(name="JSS 1")
    jss2 = Class.objects.get(name="JSS 2")
    jss3 = Class.objects.get(name="JSS 3")
    ss1 = Class.objects.get(name="SS 1")
    ss2 = Class.objects.get(name="SS 2")
    ss3 = Class.objects.get(name="SS 3")

    classes = request.user.classes.all

    class_get = request.user.student_class

    context = {
        "students": page_objects,
        'object': request.user,
        'classes': classes,
        'jss1': jss1,
        'jss2': jss2,
        'jss3': jss3,
        'ss1': ss1,
        'ss2': ss2,
        'ss3': ss3,
        "class": class_get
    }
    return render(request, "student/student_list.html", context)


def student_ss3(request):
    class_ = Class.objects.get(name="SS 3")
    students = User.objects.filter(is_student=True, school=request.user.school, student_class=class_).order_by('date_joined')
    paginator = Paginator(students, 1)
    page_number = request.GET.get('page')
    try:
        page_objects = paginator.page(page_number)
    except PageNotAnInteger:
        page_objects = paginator.page(1)
    except EmptyPage:
        page_objects = paginator.page(paginator.num_pages)

    jss1 = Class.objects.get(name="JSS 1")
    jss2 = Class.objects.get(name="JSS 2")
    jss3 = Class.objects.get(name="JSS 3")
    ss1 = Class.objects.get(name="SS 1")
    ss2 = Class.objects.get(name="SS 2")
    ss3 = Class.objects.get(name="SS 3")

    classes = request.user.classes.all

    class_get = request.user.student_class

    context = {
        "students": page_objects,
        'object': request.user,
        'classes': classes,
        'jss1': jss1,
        'jss2': jss2,
        'jss3': jss3,
        'ss1': ss1,
        'ss2': ss2,
        'ss3': ss3,
        "class": class_get
    }
    return render(request, "student/student_list.html", context)


def admin_settings(request):
    if request.user.is_admin:
        school = get_object_or_404(School, pk=request.user.school.pk)

        if request.method == 'POST':
            form = SettingsForm(request.POST, instance=school)

            if form.is_valid():
                form.save()
                sweetify.sweetalert(request, "Success!", text="Settings saved.", icon='success')
                return redirect('admin-page')
        else:
            form = SettingsForm(instance=school)

        return render(request, 'admin_/settings.html', {"form": form })
    else:
        user_admin = User.objects.get(school=request.user.school, is_admin=True)
        defaulter = Defaulters.objects.create(user=request.user, user_admin=user_admin, page=request.get_raw_uri())
        defaulter.save()
        logout(request)
        sweetify.sweetalert(request, "Warning!",
                            text="You tried accessing the settings page when you are"
                            " not an administrator, Your account information has been "
                            "sent to your admin. ", icon="warning", persistent=True)
        return redirect('home-login')


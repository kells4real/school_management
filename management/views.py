from django.shortcuts import render, HttpResponseRedirect, reverse

# Create your views here.

def redirect_view(request):
    if request.user.is_admin or request.user.is_superuser:
        return HttpResponseRedirect(
                   reverse('admin-page'))

    elif request.user.is_teacher:
        return HttpResponseRedirect(
            reverse('single-teacher', args=[request.user.username] ))

    elif request.user.is_student:
        return HttpResponseRedirect(
            reverse('single-student', args=[request.user.username]))
               # reverse('profile-detail',
               #          args=[request.user.username]))
    # else:
    #     return HttpResponseRedirect(
    #         reverse('followed-users'))


from django.contrib import admin
from .models import User, TeacherProfile, StudentProfile,\
    Profile, School, Class, AcademicYear
# from django.contrib.auth.admin import UserAdmin

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    model = User
    filter_horizontal = ('user_permissions', 'groups',)

class StudentProfileAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("user",)}

class TeacherProfileAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("user",)}

class ProfileAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("user",)}

admin.site.register(User, UserAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(TeacherProfile, TeacherProfileAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(School)
admin.site.register(Class)
admin.site.register(AcademicYear)
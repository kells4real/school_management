from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StudentProfile, TeacherProfile, Profile
from django.conf import settings

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_student:
            StudentProfile.objects.create(user=instance)
        elif instance.is_teacher:
            TeacherProfile.objects.create(user=instance)
        else:
            Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_profile(sender, instance, **kwargs):
    if instance.is_student:
        instance.studentprofile.save()
    elif instance.is_teacher:
        instance.teacherprofile.save()
    else:
        instance.profile.save()


from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.text import slugify
from PIL import Image
from results.models import Subject, AcademicYear
import moneyed
from djmoney.models.fields import MoneyField


class Plan(models.Model):
    title = models.CharField(max_length=30)
    limit = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)


def user_upload(instance, filename):
    username = instance.username
    slug = slugify(username)
    return f"user_pics/{slug}/{filename}"


class Class(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Classes"

class School(models.Model):
    name = models.CharField(max_length=150, null=True)
    address = models.CharField(max_length=150, null=True)
    date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    teacher_can_view_student_details = models.BooleanField(default=True)
    student_can_view_student_details = models.BooleanField(default=False)
    student_can_send_message = models.BooleanField(default=False)
    teacher_can_send_student_message = models.BooleanField(default=False)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)
    date_of_birth = models.DateField(null=True)
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='studentprofile', null=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='student_profile', null=True)

    CHR = 'Christian'
    MUS = 'Muslim'
    OTH = "Other"

    rel = (
        (CHR, 'Christian'),
        (MUS, 'Muslim'),
        (OTH, 'Other'),
    )

    religion = models.CharField(
        max_length=100,
        choices=rel,
        null=True
    )


    # Teacher Specific
    date_employed = models.DateField(null=True)
    subject = models.ManyToManyField(Subject)
    salary = MoneyField(max_digits=10, decimal_places=2, default_currency='NGN', null=True, blank=True)
    phone_no = models.CharField(max_length=50, null=True)
    classes = models.ManyToManyField(Class)

    # Student Specific
    mother_name = models.CharField(max_length=50, null=True)
    mother_number = models.CharField(max_length=50, null=True)
    father_name = models.CharField(max_length=50, null=True)
    father_number = models.CharField(max_length=50, null=True)

    address = models.CharField(max_length=100, null=True)

    MALE = 'Male'
    FEMALE = 'Female'

    sex = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),

    )

    gender = models.CharField(
        max_length=100,
        choices=sex,
        null=True
    )

    image = models.ImageField(default='default-profile-picture.jpg', upload_to=user_upload, null=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True)
    disabled = models.BooleanField(default=False)
    # Profile.objects.filter(ratings__isnull=False).order_by('ratings__average')

    def __str__(self):
        return f'{self.user.username} Profile'

    def _get_unique_slug(self):
        slug = slugify(self.user)
        unique_slug = slug
        num = 1
        if StudentProfile.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class TeacherProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True)
    disabled = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'

    def _get_unique_slug(self):
        slug = slugify(self.user)
        unique_slug = slug
        num = 1
        if TeacherProfile.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"

    def _get_unique_slug(self):
        slug = slugify(self.user)
        unique_slug = slug
        num = 1
        if TeacherProfile.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
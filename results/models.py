from django.db import models
from django.conf import settings

# Create your models here.

class AcademicYear(models.Model):
    year = models.CharField(max_length=50)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.year

class Term(models.Model):
    name = models.CharField(max_length=30, null=True)
    active = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.name

class Grade(models.Model):
    first_test = models.FloatField(null=True)
    second_test = models.FloatField(null=True)
    exam = models.FloatField(null=True)
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='grade_term', null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='grade_user', null=True)
    subject = models.ForeignKey(Subject, related_name="grade_subject", on_delete=models.CASCADE, null=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name="grade_academic_year", null=True)


    def __str__(self):
        return f"{self.user} grades for {self.subjects}, {self.term}"


# class Result(models.Model):
#     pass


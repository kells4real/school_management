from django.db import models
from django.conf import settings

# Create your models here.


class RegistrationLinks(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    link = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.user} activation link"


class Defaulters(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
    user_admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_admin")
    page = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} {self.date}"

    class Meta:
        verbose_name_plural = "Defaulters"



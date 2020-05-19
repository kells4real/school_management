from django.urls import path
from .views import single_teacher

urlpatterns = [
    path('<slug>/', single_teacher, name="single-teacher")
]
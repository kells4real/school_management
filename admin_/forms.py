from django import forms
import re
from management.models import User, School

class StudentRegisterForm(forms.ModelForm):
    username = forms.RegexField(regex=re.compile(r'^[A-Za-z0-9_.-]{4,30}$'), required=True,
                     error_messages={'invalid': "Username must be between 4 and 30 alphanumeric characters including _ or ."}, label="Username")
    mother_number = forms.RegexField(regex=re.compile(r'^[0-9+]{10,15}$'), required=False,
                     error_messages={'invalid': "Enter a valid phone number"}, label="Phone No")
    father_number = forms.RegexField(regex=re.compile(r'^[0-9+]{10,15}$'), required=False,
                     error_messages={'invalid': "Enter a valid phone number"}, label="Phone No")
    date_of_birth = forms.DateField(
    widget=forms.TextInput(
        attrs={'type': 'date', 'title': 'Date of birth'}
    )
)

    email = forms.EmailField(max_length=200)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'student_class', 'gender',
                  'academic_year', 'image', 'password', 'password2', 'mother_name', 'mother_number', 'father_name',
                  'father_number', 'address', 'religion')

        labels = {
            'first_name': "First name(s)",
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Please use another Email, this Email has already been used by another user.')
        return email

class AdminRegisterForm(forms.ModelForm):
    username = forms.RegexField(regex=re.compile(r'^[A-Za-z0-9_.-]{4,30}$'), required=True,
                     error_messages={'invalid': "Username must be between 4 and 30 alphanumeric characters including _ or ."}, label="Username")
    email = forms.EmailField(max_length=200, help_text='Required')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'school', 'image', 'password', 'password2')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Please use another Email, this Email has already been used by another user.')
        return email


class TeacherRegisterForm(forms.ModelForm):
    username = forms.RegexField(regex=re.compile(r'^[A-Za-z0-9_.-]{4,30}$'), required=True,
                     error_messages={'invalid': "Username must be between 4 and 30 alphanumeric characters including _ or ."}, label="Username")
    email = forms.EmailField(max_length=200, help_text='Required')
    phone_no = forms.RegexField(regex=re.compile(r'^[0-9+]{10,15}$'), required=False,
                                     error_messages={'invalid': "Enter a valid phone number"}, label="Phone No")
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    date_employed = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date', 'title': 'Date employed'}
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'religion', 'subject',
                  'salary', 'image', 'password', 'password2', 'address', 'date_employed',
                  'phone_no', 'gender', 'classes')

        labels = {
            "subject": "Subject(s)"
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Please use another Email, this Email has already been used by another user.')
        return email


class UpdateStudentRegisterForm(forms.ModelForm):
    mother_number = forms.RegexField(regex=re.compile(r'^[0-9+]{10,15}$'), required=False,
                     error_messages={'invalid': "Enter a valid phone number"}, label="Phone No")
    father_number = forms.RegexField(regex=re.compile(r'^[0-9+]{10,15}$'), required=False,
                     error_messages={'invalid': "Enter a valid phone number"}, label="Phone No")
    date_of_birth = forms.DateField(
    widget=forms.TextInput(
        attrs={'type': 'date', 'title': 'Date of birth'}
    )
)

    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'date_of_birth', 'student_class', 'gender',
                  'academic_year', 'image', 'mother_name', 'mother_number', 'father_name',
                  'father_number', 'address', 'religion',)

        labels = {
            'first_name': "First name(s)",
        }


class UpdateTeacherRegisterForm(forms.ModelForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    phone_no = forms.RegexField(regex=re.compile(r'^[0-9+]{10,15}$'), required=False,
                                     error_messages={'invalid': "Enter a valid phone number"}, label="Phone No")
    date_employed = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date', 'title': 'Date employed'}
        )
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'religion', 'subject',
                  'salary', 'image', 'address', 'date_employed',
                  'phone_no', 'gender', 'classes')

        labels = {
            "subject": "Subject(s)"
        }


class SettingsForm(forms.ModelForm):

    class Meta:
        model = School
        fields = ["name", "student_can_send_message", "teacher_can_send_student_message",
                  "student_can_view_student_details", "teacher_can_view_student_details"]

        labels = {
            "name": "School Name",
            "student_can_view_student_details": "Students can view other students details",
            "student_can_send_message": "Students can send other students messages",
            "teacher_can_view_student_details": "Teacher can view student details",
            "teacher_can_send_student_message": "Teacher can send students messages"
        }

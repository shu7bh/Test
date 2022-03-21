from django import forms
from .models import Student,Teacher
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class RegistrationForm(forms.Form):
    OPTIONS = (
        ('Student','Student'),
        ('Teacher','Teacher'),
    )

    user_type = forms.ChoiceField(choices=OPTIONS)

    def get_form_class(self):
        if self.cleaned_data['user_type'] == 'Student':
            return StudentRegister
        elif self.cleaned_data['user_type'] == 'Teacher':
            return TeacherRegister
        else:
            return None

    def get_context_data(self, **kwargs):
        context = super(RegistrationForm, self).get_context_data(**kwargs)

        context['user_type'] = self.cleaned_data['user_type']
        return context



class StudentRegister(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(label='Email')
    class Meta:
        model = Student

        fields = ['name', 'age', 'email', 'phone', 'grade', 'school', 'password', 'confirm_password']
        labels = {
            'name': 'Full Name',
            'age': 'Age',
            'email': 'Email',
            'phone': 'Phone',
            'grade': 'Grade',
            'school': 'School',
            'password': 'Password',
            'confirm_password': 'Confirm Password',
        }

    def clean(self):
        cleaned_data = super(StudentRegister, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords don't match")

        return cleaned_data

class TeacherRegister(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(label='Email')

    class Meta:
        model = Teacher
        fields = ['name', 'email', 'password','confirm_password','phone', 'languages', 'subjects']
        labels = {
            'name': 'Full Name',
            'email': 'Email',
            'password': 'Password',
            'confirm_password': 'Confirm Password',
            'phone': 'Phone',
            'languages': 'Languages',
            'subjects': 'Subjects',
            }

    def clean(self):
        cleaned_data = super(TeacherRegister, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords don't match")

        return cleaned_data

class StudentLogin(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = ['email', 'password']
        labels = {
            'email': 'Email',
            'password': 'Password',
        }

    def clean(self):
        cleaned_data = super(StudentLogin, self).clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        pwd = 'scenes'.encode()
        salt = b'/\xb5w>`&\x86\x86\x05\x85\xec^\xba\x0cZ\x1a'

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )

        key = base64.urlsafe_b64encode(kdf.derive(pwd))
        fernet = Fernet(key)

        if email and password:
            try:
                student = Student.objects.get(email=email)
                if fernet.decrypt(student.password.encode()).decode() == password:
                    return cleaned_data
                else:
                    self.add_error('password', "Incorrect password")
            except Student.DoesNotExist:
                self.add_error('email', "Email does not exist")
        else:
            self.add_error('email', "Email or password is missing")

        return cleaned_data

class TeacherLogin(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = ['email', 'password']
        labels = {
            'email': 'Email',
            'password': 'Password',
        }

    def clean(self):
        cleaned_data = super(TeacherLogin, self).clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        pwd = 'scenes'.encode()
        salt = b'/\xb5w>`&\x86\x86\x05\x85\xec^\xba\x0cZ\x1a'

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )

        key = base64.urlsafe_b64encode(kdf.derive(pwd))
        fernet = Fernet(key)

        if email and password:
            try:
                teacher = Teacher.objects.get(email=email)
                if teacher:
                    if fernet.decrypt(teacher.password.encode()).decode() == password:
                        return cleaned_data
                    else:
                        self.add_error('password', "Incorrect password")
                else:
                    self.add_error('email', "Email does not exist")
            except Teacher.DoesNotExist:
                self.add_error('email', "Email does not exist")
        else:
            self.add_error('email', "Email or password is missing")
        return cleaned_data

from django.shortcuts import render, redirect
import base64
from .forms import StudentLogin, TeacherLogin, StudentRegister,TeacherRegister
from django.contrib import messages
from django.contrib.auth import get_user_model
# from django_email_verification import sendConfirm
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import simplejson as json

def index(request):
    return render(request, 'home.html')

def encrypt(password):
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
    return fernet.encrypt(password.encode()).decode()

def teacherLoginForm(request):
    if request.method == "POST":
        form = TeacherLogin(request.POST)
        if form.is_valid():
            return redirect('/teacher-dashboard/')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = TeacherLogin()
    return render(request, 'teacherLogin.html', {'form': form})

def studentLoginForm(request):
    if request.method == "POST":
        form = StudentLogin(request.POST)
        if form.is_valid():
            return redirect('/student-dashboard/')
            # return render(request, 'studentDashboard.html')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = StudentLogin()
    return render(request, 'studentLogin.html', {'form': form})

def studentRegForm(request):
    if request.method == "POST":
        form = StudentRegister(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.password = encrypt(form.cleaned_data['password'])
            user.save()
            return redirect('/student-dashboard/')
        else:
            messages.error(request, 'Invalid form submission.')
            messages.error(request, form.errors)
    else:
        form = StudentRegister()
    return render(request, 'studentRegistration.html', {'form': form})

def teacherRegForm(request):
    if request.method == "POST":
        form = TeacherRegister(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.password = encrypt(form.cleaned_data['password'])
            subjects = form.cleaned_data['subjects'].split(',')
            allSubjects = []
            for subject in subjects:
                if subject not in allSubjects:
                    allSubjects.append(subject)
            user.subjects = json.dumps(allSubjects)
            languages = form.cleaned_data['languages'].split(',')
            allLanguages = []
            for language in languages:
                if language not in allLanguages:
                    allLanguages.append(language)
            user.languages = json.dumps(allLanguages)
            user.save()
            return redirect('/teacher-dashboard/')
        else:
            messages.error(request, 'Invalid form submission.')
            messages.error(request, form.errors)
    else:
        form = TeacherRegister()
    return render(request, 'TeacherRegistration.html', {'form': form})

def studentDashboard(request):
    return render(request, 'studentDashboard.html')

def teacherDashboard(request):
    return render(request, 'teacherDashboard.html')


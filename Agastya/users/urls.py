from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.index, name='index'),
    path("student-register/", views.studentRegForm, name="form"),
    path("teacher-register/", views.teacherRegForm,name="form"),
    path("teacher-login/", views.teacherLoginForm, name="login"),
    path("student-login/", views.studentLoginForm, name="login"),
    path('student-dashboard/', views.studentDashboard, name='dashboard'),
    path('teacher-dashboard/', views.teacherDashboard, name='dashboard'),
]

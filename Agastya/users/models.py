from sqlite3 import Timestamp
from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    grade = models.CharField(max_length=100)
    password = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    phone = models.CharField(max_length=100)
    languages = models.TextField(null=True)
    subjects = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def homepage(request):
    return render(request,"enroll/homepage.html")

def register(request):
    return render(request,"enroll/registration.html")

def signin(request):
    return render(request,"enroll/login.html")
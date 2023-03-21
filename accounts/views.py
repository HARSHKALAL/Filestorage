from django.shortcuts import render

def homepage(request):
    return render(request,"enroll/homepage.html")

def register(request):
    return render(request,"enroll/registration.html")
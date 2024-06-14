from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.messages import constants as messages




def index(request):
    return render(request, "login.html")

def home(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request, "index.html")

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if username and email and password:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.save()
            return redirect("/login")
    return render(request, "signin.html")

def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/home")
        else:
            return redirect("/login")
    return render(request, "login.html")

def logoutUser(request):
    logout(request)
    return redirect("/login")
            


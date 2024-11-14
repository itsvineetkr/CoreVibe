from django.shortcuts import render, redirect
from django.contrib.auth import login as login_user, logout as logout_user, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from stats.models import UserPhysicalData, UserGoals
from datetime import time


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            login_user(request, user)
            return redirect("/")
        else:
            return redirect("/login")
    return render(request, "accounts/login.html")


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if username and email and password:
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            user.save()
            login_user(request, user)
            return redirect("/details")
        else:
            messages.error("Enter correct details!")
    return render(
        request,
        "accounts/signup.html",
    )


def logout(request):
    logout_user(request)
    return redirect("/login")


def details(request):
    user = request.user
    
    if user.is_anonymous:
        return redirect("/login")

    if request.method == "POST":
        height = int(request.POST.get("height"))
        weight = int(request.POST.get("weight"))
        age = int(request.POST.get("age"))
        gender = request.POST.get("gender")

        steps = int(request.POST.get("steps"))
        water = int(request.POST.get("water"))
        active_minutes = int(request.POST.get("active"))
        kcal = int(request.POST.get("kcal"))
        no_of_hours = int(request.POST.get("sleep"))
        sleep_hours = time(hour=no_of_hours)

        UserGoals(
            user = user,
            steps = steps,
            water = water,
            active = active_minutes,
            kcal = kcal,
            sleep = sleep_hours
        ).save()

        UserPhysicalData(
            user=user, height=height, weight=weight, age=age, gender=gender
        ).save()

        return redirect("/login")
    return render(request, "accounts/details.html")

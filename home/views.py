from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.messages import constants as messages
from home.models import UserGoals, UserDailyStats, UserStaticStats, UserMood
from datetime import datetime
import ollama
ollama.pull('phi3:mini')



def index(request):
    return render(request, "login.html")


def home(request):
    if request.user.is_anonymous:
        return redirect("/login")
    
    username = request.user.username
    data = UserDailyStats.objects.filter(username = username)[0].data[str(datetime.now().date())]
    goals = UserGoals.objects.filter(username = username)[0].data
    steps = data[0]
    water = data[1]
    active = data[2]
    kcal = data[3]
    sleephr = data[4]//60
    sleepmin = data[4]%60
    gsteps = goals[0]
    gwater = goals[1]
    gactive = goals[2]
    gkcal = goals[3]    
    
    data = UserStaticStats.objects.filter(username = username)[0].data

    height = data[0]
    weight = data[1]
    age = data[2]
    gender = data[3]

    bmi = round(weight/((height/100)**2),2)

    pbmi = (bmi/30)*100

    if pbmi>30:
        pbmi = 30
    
    aih, hwmd = '', ''

    if request.method == "POST":
        if 'waterPost' in request.POST:
            todayData = UserDailyStats.objects.filter(username = username)[0]
            dataDict = todayData.data
            dataDict[str(datetime.now().date())][1] += 250
            todayData.data = dataDict
            todayData.save()
            return redirect("/home")
        elif 'aihPost' in request.POST:
            message = f"If my age is {age}, gender is {gender}, weight is {weight} and height is {height} and today I walked {steps} steps and burned {kcal} calories, Am I healthy?. Generate a small and concise response."
            stream = ollama.generate(model = "phi3:mini", prompt=message)
            aih = stream["response"] 
        elif 'hwmdPost' in request.POST:
            message = f"If my age is {age}, gender is {gender}, weight is {weight} and height is {height} and today I walked {steps} steps, burned {kcal} calories, drank {water} ml Water and was active for {active} mins, how was my day so far according to this data?. Generate a small and concise response."
            stream = ollama.generate(model = "phi3:mini", prompt=message)
            hwmd = stream["response"]
        elif 'mood_value' in request.POST:
            todayData = UserMood.objects.filter(username = username)[0]
            dataDict = todayData.data
            dataDict[str(datetime.now())] = request.POST.get("mood_value")
            todayData.data = dataDict
            todayData.save()
            return redirect("/home")

    context = {
        'steps' : steps,
        'water' : water,
        'active' : active,
        'kcal' : kcal,
        'sleephr' : sleephr,
        'sleepmin' : sleepmin,
        'gsteps' : gsteps,
        'gwater' : gwater,
        'gactive' : gactive,
        'gkcal' : gkcal,
        'psteps' : (steps/gsteps)*100,
        'pwater' : (water/gwater)*100,
        'pactive' : (active/gactive)*100,
        'pkcal' : (kcal/gkcal)*100,
        'hwmd' : hwmd,
        'aih' : aih,
        'bmi' : bmi,
        'pbmi' : pbmi,
        'weight' : weight
    }

    return render(request, "index.html", context = context)


def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            if username and email and password:

                user = User.objects.create_user(
                    username=username, email=email, password=password
                )
                user.save()

                dailyStats = UserDailyStats(username = username, data = {str(datetime.now().date()):[0,0,0,0,0]})
                dailyStats.save()

                goals = UserGoals(username = username, data = [6000, 2000, 60, 500])
                goals.save()

                mood = UserMood(username = username, data = {})
                mood.save()

                return redirect("/details")
            
        except:
            return render(
                request,
                "signin.html",
                context={
                    "userAlreadyExist": "Username already exists!",
                    "tryAnother": "try another username",
                },
            )
    return render(request, "signin.html")


def loginUser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

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

def details(request):
    print(request.POST.get("username"), "<=== this is a data")
    username = User.objects.all().last().username
    if request.method == "POST":

        height = int(request.POST.get("height"))
        weight = int(request.POST.get("weight"))
        age = int(request.POST.get("age"))
        gender = request.POST.get("gender")
        
        staticStats = UserStaticStats(username = username, data = [height, weight, age, gender])
        staticStats.save()

        return redirect("/login")
    return render(request, "details.html")
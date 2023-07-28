from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import Period
from .forms import *
from .features import *

from datetime import datetime, timedelta


def index(request):
    if not request.user.is_authenticated:
        return redirect('period_tracker:login')
    return redirect('period_tracker:user')
    
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid:
            form.save()
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('period_tracker:index')
    return render(request, "period_tracker/register.html",{
        "form": CustomUserCreationForm()
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('period_tracker:index')
        else:
            return render(request, "period_tracker/login.html", {
                "message": "Niepoprawne dane logowania."
            })
    return render(request, "period_tracker/login.html")
    

def logout_view(request):
    logout(request)
    return render(request, "period_tracker/login.html", {
        "message": "Wylogowano."
    })


def user(request):
    length = mean_length(request.user)
    next = next_period(request.user, mean_length)

    return render(request, "period_tracker/user.html", {
        "next_period": next,
        "mean_length": length,
    })

def add_period(request):
    if request.method == "POST":
        form = PreviousPeriodForm(request.POST)
        if form.is_valid():
            period = form.save(commit=False)
            period.user = request.user
            period.save()

            periods = Period.objects.filter(user=request.user).order_by("-first_day")

            period_1 = periods[0]
            period_2 = periods[1]
            length = (period_1.first_day - period_2.first_day).days
            period_2.length = length
            period_2.save()

    return render(request, "period_tracker/add_period.html",{
        "periods": Period.objects.filter(user=request.user).order_by("first_day"),
        "form": PreviousPeriodForm,
    })

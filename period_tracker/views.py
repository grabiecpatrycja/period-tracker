from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError
from django.shortcuts import render, redirect
from datetime import date
from .forms import *
from .features import *

def index(request):
    if not request.user.is_authenticated:
        return redirect('period_tracker:login')
    return redirect('period_tracker:user')
    
def register(request):
    form = CustomUserCreationForm()
    errors = None
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST["username"]
            password = request.POST["password1"]
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('period_tracker:log_period')
        else:
            errors = form.errors
    return render(request, "period_tracker/register.html", {
        "form": form,
        "errors": errors
    })

def login_view(request):
    form = AuthenticationForm()
    message = None
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('period_tracker:index')
        else:
            message = "Invalid credentials."
    return render(request, "period_tracker/login.html", {
        "form": form,
        "message": message
    })

def logout_view(request):
    logout(request)
    return render(request, "period_tracker/login.html", {
        "form": AuthenticationForm(),
        "message": "Logged out"
    })

def user(request):
    try:
        day = date.today() - last_period(request.user).first_day + timedelta(days=1)
        next = next_period(request.user)
        day_to_next = next - date.today()
        next_ovul = next_ovulation(request.user)
        day_to_ovul = next_ovul - date.today()
        avg_length = average_length(request.user)
        avg_ovulation = average_ovulation(request.user)
        return render(request, "period_tracker/user.html", {
            "day": day,
            "next_period": next,
            "day_to_next": day_to_next,
            "next_ovulation": next_ovul,
            "day_to_ovul": day_to_ovul,
            "average_length": avg_length,
            "average_ovulation": avg_ovulation
        })
    except AttributeError:
        return redirect('period_tracker:log_period')

def history(request):
    periods = calculate_lengths(request.user)
    return render(request, "period_tracker/history.html", {
        "periods": periods
    })

def log_period(request):
    form = PeriodForm()
    message = None

    if request.method == "POST":
        form = PeriodForm(request.POST)
        if form.is_valid():
            try:
                period = form.save(commit=False)
                period.user = request.user

                ovulation_day = form.cleaned_data['ovulation_day']
                first_day = form.cleaned_data['first_day']
                if ovulation_day is None or ovulation_day > first_day:
                    form.save()
                    return redirect('period_tracker:user')
                else:
                    message = 'The ovulation day you trying to assign is before the first day of current cycle!'
            except IntegrityError:
                message = "You've already added this cycle."
    return render(request, "period_tracker/log_period.html", {
        "form": form,
        "message": message
        })

def log_ovulation(request):
    period = last_period(request.user)
    message = None

    if request.method == "POST": 
        form = PeriodForm(request.POST, instance=period, initial={'first_day': period.first_day})
        form.fields['first_day'].widget = forms.HiddenInput()
        if form.is_valid():
            if form.cleaned_data['ovulation_day'] > period.first_day:
                form.save()
                return redirect('period_tracker:user')
            else:
                message = 'The ovulation day you trying to assign is before the first day of current cycle!'
    else:
        form = PeriodForm(instance=period)
        form.fields['first_day'].widget = forms.HiddenInput()
    return render(request, "period_tracker/log_ovulation.html", {
        "form": form,
        "message": message
        })
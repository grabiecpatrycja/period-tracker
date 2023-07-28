from django.contrib.auth.models import User
from .models import Period
from datetime import date, timedelta
from statistics import mean

def mean_length(user):
    periods = Period.objects.filter(user=user)
    lengths = [period.length for period in periods]
    return round(mean(lengths))

def next_period(user, mean_length):
    last_period = Period.objects.filter(user=user).latest("first_day")
    next_period = last_period.first_day + timedelta(days=mean_length)
    return next_period
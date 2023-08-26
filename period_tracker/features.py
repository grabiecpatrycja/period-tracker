from django.db.models import Subquery, OuterRef, F, Avg
from .models import Period
from datetime import date, timedelta


def calculate_lengths(user):
    previous_period = Subquery(Period.objects.filter(user=OuterRef('user'), first_day__lt=OuterRef('first_day')).order_by('-first_day').values('first_day')[:1])
    periods = Period.objects.filter(user=user).order_by('-first_day').annotate(length=F('first_day')-previous_period).annotate(ovulation_len=F('ovulation_day')-F('first_day')+timedelta(days=1))
    return periods

def average_length(user):
    periods = calculate_lengths(user)
    average_length = periods.aggregate(avg_length=Avg(F('length')))
    return average_length

def average_ovulation(user):
    periods = calculate_lengths(user)
    average_ovulation = periods.aggregate(avg_ovulation=Avg(F('ovulation_len')))
    return average_ovulation

def last_period(user):
    last_period = Period.objects.filter(user=user).order_by('-first_day').first()
    return last_period

def next_period(user):
    last = last_period(user)
    avg_length = average_length(user)
    average = avg_length['avg_length']
    if average is None:
        average = timedelta(days=28)

    next_period = last.first_day + average
    return next_period

def next_ovulation(user):
    period = last_period(user)
    avg_ovulation = average_ovulation(user)
    average = avg_ovulation['avg_ovulation'] - timedelta(days=1)
    if average is None:
        average = timedelta(days=13)

    if date.today() <= (period.first_day + average):
        next_ovulation = period.first_day + average
    else:
        next = next_period(user)
        next_ovulation = next + average
    return next_ovulation

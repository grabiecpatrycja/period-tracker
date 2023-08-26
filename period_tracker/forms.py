from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Period

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "email", "password1", "password2"]

class PeriodForm(forms.ModelForm):
    class Meta:
        model = Period
        fields = ["first_day", "ovulation_day"]
        widgets = {
            'first_day': forms.DateInput(attrs={'type':'date', 'class': 'date-input'}),
            'ovulation_day': forms.DateInput(attrs={'type':'date', 'class': 'date-input'})
        }


    def __init__(self, *args, **kwargs):
        super(PeriodForm, self).__init__(*args, **kwargs)
        self.fields["ovulation_day"].required = False

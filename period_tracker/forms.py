from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Period

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "email", "password1", "password2"]

class PreviousPeriodForm(forms.ModelForm):
    class Meta:
        model = Period
        fields = ["first_day", "ovulation_day"]

    def __init__(self, *args, **kwargs):
        super(PreviousPeriodForm, self).__init__(*args, **kwargs)
        self.fields["ovulation_day"].required = False
from . import views
from django.urls import path

app_name = "period_tracker"
urlpatterns = [
    path("", views.index, name='index'),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("user", views.user, name="user"),
    path("history", views.history, name="history"),
    path("log_period", views.log_period, name="log_period"),
    path("log_ovulation", views.log_ovulation, name="log_ovulation")
]
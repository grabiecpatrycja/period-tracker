from . import views
from django.urls import path

app_name = "period_tracker"
urlpatterns = [
    path("", views.index, name='index'),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("user", views.user, name="user"),
    path("add", views.add_period, name="add"),
]
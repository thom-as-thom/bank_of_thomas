from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("sign-up", views.sign_up, name="sign-up"),
    path("login", views.login, name="login"),
    path("onboarding", views.onboarding, name="onboarding"),
    path("dashboard", views.dashboard, name="dashboard"),
]

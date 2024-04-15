from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("sign-up", views.sign_up, name="sign-up"),
    path("login", views.login, name="login"),
    path("onboarding", views.onboarding, name="onboarding"),
    path("logout", views.logout, name="logout"),
]

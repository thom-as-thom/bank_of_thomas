from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, ProfileForm, EmploymentForm, InvestmentForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, logout, authenticate
from django.templatetags.static import static
from django.contrib.auth.models import User
from .models import Profile
from .models import OnboardingStep


# Create your views here.


def checkAuth(request):
    if not request.user.is_authenticated:
        return redirect("login")
    user = request.user
    profile = user.profile if hasattr(user, "profile") else None
    return [user, user.profile]

def sign_up(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "register.html", {"form": form})


def login(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def onboarding(request):
    user, profile = checkAuth(request)

    current_step = (
        OnboardingStep(profile.onboarding_step)
        if profile
        else OnboardingStep.PERSONAL_INFO
    )

    onboarding_steps = list(OnboardingStep)
    current_index = onboarding_steps.index(current_step)
    if current_index < len(onboarding_steps) - 1:
        onboarding_step = onboarding_steps[current_index + 1]

    profileForms = {
        OnboardingStep.PERSONAL_INFO: ProfileForm,
        OnboardingStep.EMPLOYMENT_INFO: EmploymentForm,
        OnboardingStep.INVESTMENT_INFO: InvestmentForm,
    }.get(current_step)

    if request.method == "POST":
        form = profileForms(request.POST)
        if form.is_valid():
            defaults = form.cleaned_data
            profile, created = Profile.objects.update_or_create(
                user=request.user,
                defaults={
                    **defaults,
                    "onboarding_step": onboarding_step.value,
                },
            )
            return redirect("onboarding")
    if profile.onboarding_step == OnboardingStep.COMPLETE.value:
        return redirect("home")

    form = profileForms()

    return render(request, "onboarding.html", {"form": form})


def dashboard(request):
    user, profile = checkAuth(request)
    accounts = user.accounts.all()
    return render(
        request,
        "dashboard/dashboard.html",
        {"user": user, "profile": profile, "accounts": accounts},
    )

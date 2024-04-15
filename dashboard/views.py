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


def home(request):
    banner1_context = {
        "super_title": "What are you waiting for to start referring and enjoy the benefits of T-Bank?",
        "title": "With referrals you can also travel!",
        "sub_title": "Choose T-Bank Points or credit balance on your credit card",
        "cta": "Learn more",
        "cta_href": "#",
        "image_url": static("images/image-36.jpg"),
    }
    banner2_context = {
        "sub_title": "Get to know our insurance",
        "title": "T-Bank car insurance",
        "sub_title": "You have up to 50 percent discount on the first installments. Hire it or quote it fully online. Choose the plan that best suits your needs, and that's it!",
        "cta": "Learn more",
        "cta_href": "#",
        "image_url": static("images/image-37.jpg"),
    }
    carrousel_content = [
        {
            "title": "Invest",
            "image_url": static("images/image-38.jpg"),
        },
        {
            "title": "Banking services for your company",
            "image_url": static("images/image-39.jpg"),
        },
        {
            "title": "Purchase life insurance",
            "image_url": static("images/image-40.jpg"),
        },
        {
            "title": "Request your mortgage loan",
            "image_url": static("images/image-42.jpg"),
        },
        {
            "title": "Open a savings account",
            "image_url": static("images/image-43.jpg"),
        },
        {
            "title": "Request a credit card",
            "image_url": static("images/image-44.jpg"),
        },
    ]
    return render(
        request,
        "home.html",
        {
            "banner1": banner1_context,
            "banner2": banner2_context,
            "carrousel": carrousel_content,
        },
    )


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
    return render(
        request, "dashboard/dashboard.html", {"user": user, "profile": profile}
    )

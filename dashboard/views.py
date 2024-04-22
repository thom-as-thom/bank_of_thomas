from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, ProfileForm, EmploymentForm, InvestmentForm
from django.contrib.auth import login, authenticate
from .models import Profile
from .models import OnboardingStep
from bank_of_thomas.utils import checkAuth
from accounts.utils import card_options, account_options


# Create your views here.


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
    cards = user.cards.all()
    accounts_info = []
    for account in accounts:
        accounts_info.append(
            {
                "name": account.account_type.capitalize() + " account ",
                "subname": str(account.account_number)[-4:],
                "amount": account.balance,
                "main_options": account_options["main_options"],
                "dropdown_options": account_options["dropdown_options"],
            }
        )
    cards_info = []
    for card in cards:
        cards_info.append(
            {
                "subname": str(card.card_number)[-4:],
                "type": card.card_type,
                "name": card.card_provider,
                "amount": card.amount_due if hasattr(card, "amount_due") else None,
                "main_options": card_options[card.card_type.lower()]["main_options"],
                "dropdown_options": card_options[card.card_type.lower()][
                    "dropdown_options"
                ],
            }
        )
    return render(
        request,
        "dashboard/dashboard.html",
        {
            "user": user,
            "profile": profile,
            "accounts": accounts_info,
            "cards": cards_info,
        },
    )

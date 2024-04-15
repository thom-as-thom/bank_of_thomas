from django.shortcuts import render
from .forms import CreateBankAccountForm


# Create your views here.
def create_account(request):
    if request.method == "POST":
        form = CreateBankAccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return render(request, "account_created.html")
    return render(request, "create_account.html", {"form": CreateBankAccountForm()})

from django.shortcuts import redirect


def checkAuth(request):
    if not request.user.is_authenticated:
        return redirect("login")
    user = request.user
    profile = user.profile if hasattr(user, "profile") else None
    return [user, profile]

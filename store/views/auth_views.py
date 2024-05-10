from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from ..forms import RegistrationForm
from ..utils.date_utils import get_user_time


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("product_list")
    return render(request, "auth/logout.html")


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile")
    else:
        form = RegistrationForm()
    return render(request, "auth/register.html", {"form": form})


@login_required
def profile_view(request):
    user = request.user
    user_time_data = get_user_time()
    context = {"user": user, "user_time_data": user_time_data}
    return render(request, "auth/profile.html", context)

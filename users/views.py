from django.shortcuts import render

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)          # сразу входим после регистрации
        return redirect("home:index")
    return render(request, "users/register.html", {"form": form})

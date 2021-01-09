from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views

# Create your views here.


def home(request):
    return render(request, "index.html", {})


def login(request):
    if request.user.is_authenticated:
        return redirect("/")

    return auth_views.LoginView.as_view()(request)

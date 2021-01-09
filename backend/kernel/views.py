from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Create your views here.


def home(request):
    return render(request, "index.html", {})


def login(request):
    if request.user.is_authenticated:
        return redirect("/")

    return auth_views.LoginView.as_view()(request)


class Scores(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        return Response({"message": "Hey!"})

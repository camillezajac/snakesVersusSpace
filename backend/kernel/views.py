from django.core import serializers
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import ScoreModel

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
        try:
            username = request.data["username"]

            user = User.objects.filter(username=username).first()
            res = ScoreModel.objects.filter(
                user=user.id).order_by("score").all()
            data = serializers.serialize("json", res)

            return Response({"success": "true", "data": data})
        except Exception:
            return Response({"success": "false"})

    def post(self, request):
        try:
            username = request.data["username"]
            score = int(request.data["score"])
            accuracy = float(request.data["accuracy"])
            time_s = float(request.data["time_s"])

            user = User.objects.filter(username=username).first()
            ScoreModel(user=user,
                       score=score,
                       accuracy=accuracy,
                       time_s=time_s).save()

            return Response({"success": "true"})
        except Exception as e:
            print("HERE", e)
            return Response({"success": "false"})

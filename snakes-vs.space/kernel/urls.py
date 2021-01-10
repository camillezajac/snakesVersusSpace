from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("", views.home),
    path("login/", views.login),
    path("api/token/", jwt_views.TokenObtainPairView.as_view()),
    path("api/token/refresh", jwt_views.TokenRefreshView.as_view()),
    path("scores/", views.Scores.as_view()),
]

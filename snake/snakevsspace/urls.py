from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name="snake-home"), #empty first argument defaults to homepage
]
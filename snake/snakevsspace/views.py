from django.shortcuts import render
from django.http import HttpResponse

# handle request sent when visitor goes to homepage
def home(request):
	return HttpResponse('<h1>Snakes vs Space</h1>')
from django.shortcuts import render
from WeatherSTUFF.models import Pin, UserProfile

def index(request):
	return render(request, 'WeatherSTUFF/index.html')
	
def my_account(request):
	return render(request, 'WeatherSTUFF/myaccount.html')

def change_details(request):
	return render(request, 'WeatherSTUFF/changedetails.html')

def about(request):
	return render(request, 'WeatherSTUFF/about.html')

def sign_up(request):
	return render(request, 'WeatherSTUFF/register.html')

def sign_in(request):
	return render(request, 'WeatherSTUFF/login.html')



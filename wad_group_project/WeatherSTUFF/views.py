from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core import serializers
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from WeatherSTUFF.forms import UserForm, UserProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

import datetime

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

# Recieve a pin post request, save pin to server
def add_pin(request):
    if request.method == 'POST':
        datenow = datetime.datetime.now() # python wants the date in an exact format
        print("Request user:" + str(request.user))
        try:
            if(request.user.is_authenticated):
                userProf = UserProfile.objects.filter(user__exact=request.user)
            else:
                raise UserProfile.DoesNotExist
        except UserProfile.DoesNotExist:
            return HttpResponse(status=401, content="No User found, you are not logged in.")
            #raise Http404("No User found, you are not logged in.")
        p = Pin(  \
        user = userProf, \
        date = datenow, \
        x_val = request.POST['lat'], \
        y_val = request.POST['lng'], \
        title = request.POST['title'], \
        content = request.POST['content'], \
        )
        p.save()
        return HttpResponse(status=201)

def get_pins(request):
    # Don't bother checking for anything, just
    # return a json of all the get_pins

    pin_data = serializers.serialize('json', Pin.objects.all())
    return HttpResponse(pin_data, content_type='application/json')

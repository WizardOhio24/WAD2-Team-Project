from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core import serializers
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse


import datetime

from WeatherSTUFF.models import Pin, UserProfile

#imports for user authentication
from WeatherSTUFF.forms import UserForm, UserProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def index(request):
	return render(request, 'WeatherSTUFF/index.html')

def my_account(request):
	return render(request, 'WeatherSTUFF/myaccount.html')

def change_details(request):
	return render(request, 'WeatherSTUFF/changedetails.html')

def about(request):
	return render(request, 'WeatherSTUFF/about.html')

def sign_up(request):
	registered = False

	if request.method == 'POST':
		user_form = UserForm(request.POST)
		profile_form = UserProfileForm(request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit = False)
			profile.user = user
			
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
			profile.save()

			registered = True
		else:
			print(user_form.errors, profile_form.errors)
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render(request, 'WeatherSTUFF/register.html', context = {'user_form':user_form, 'profile_form': profile_form, 'registered': registered})

def sign_in(request):

	if request.method == 'POST':
		
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username = username, password = password)
		
		if user:
			if user.is_active:
				login(request, user)
				return redirect(reverse('WeatherSTUFF:index'))
			else:
				return HttpResponse("Your account has been disabled.")
		else:
			print(f"Invalid login details: {username}, {password}")
			return render(request, 'WeatherStuff/login.html')
	else:
		return render(request, 'WeatherSTUFF/login.html')

@login_required
def restricted(request):
	return render(request, 'WeatherSTUFF/changedetails.html')

@login_required
def user_logout(request):
	logout(request)
	return redirect(reverse('WeatherSTUFF:index'))

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



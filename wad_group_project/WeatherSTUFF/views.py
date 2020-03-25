from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core import serializers
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse


import datetime

from WeatherSTUFF.models import Pin, UserProfile, FavouritePlace

#imports for user authentication
from WeatherSTUFF.forms import UserForm, UserProfileForm, DeleteProfileForm, DeletePinForm, EditUserForm, FavPlaceForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import math

def show_fav_place(request, fav_place_slug):
	
	fav_place = FavouritePlace.objects.filter(slug=fav_place_slug).first()
	form = FavPlaceForm()

	all_pins = Pin.objects.all()
	pins = []
	for pin in all_pins:
		diff_x = fav_place.x_val-pin.x_val
		diff_y = fav_place.x_val-pin.x_val
		distance = math.sqrt((diff_x**2)+(diff_y**2))
		if distance<50:
			pins.append(pin)
	
	if request.method=="POST":
		form = FavPlaceForm(request.POST)
		fav_place.delete()
		return redirect(reverse('WeatherSTUFF:myaccount'))
	return render(request, 'WeatherSTUFF/favPlace.html', context={'form':form, 'fav_place':fav_place, 'pins':pins})

def add_fav(request):
	
	userProf = UserProfile.objects.filter(user__exact=request.user).first()

	form = FavPlaceForm()

	if request.method=="POST":
		form = FavPlaceForm(request.POST)
		if form.is_valid():
			fav_place = form.save(commit=False)
			fav_place.user = userProf
			fav_place.save()
			return redirect(reverse('WeatherSTUFF:myaccount'))

	return render(request, 'WeatherSTUFF/addfav.html', context={'form':form})
	


def index(request):
	return render(request, 'WeatherSTUFF/index.html')

def show_pin(request, pin_name_slug):
	context_dict={}
	if request.method=='POST':

		if request.user.is_authenticated:
			form = DeletePinForm(request.POST)
			context_dict['form'] = form
			try:
				pin = Pin.objects.get(slug=pin_name_slug)

				context_dict['pin'] = pin

				pin.delete()

			except Pin.DoesNotExist:

				context_dict['pin'] = None
		context_dict['message'] = "You pin has been succesfully deleted"
	

	return render(request, 'WeatherSTUFF/pin.html', context=context_dict)


def my_account(request):
	if request.user.is_authenticated:
		userProf = UserProfile.objects.filter(user__exact=request.user).first()
		pins = Pin.objects.filter(user=userProf)
		fav_places = FavouritePlace.objects.filter(user=userProf)

		return render(request, 'WeatherSTUFF/myaccount.html', context={'userProf':userProf, 'pins':pins, 'fav_places':fav_places})
	else:
		return render(request, 'WeatherSTUFF/myaccount.html')

# Edit an existing account
def change_details(request):
	if request.method=='POST':
		user_form = EditUserForm(request.POST, instance=request.user)
		user_form.actual_user = request.user
		if user_form.is_valid():
			user_form.save()
			
			return redirect(reverse('WeatherSTUFF:myaccount'))
	else:
		user_form = EditUserForm(request.POST, instance=request.user)
	context_dict = {'user_form':user_form}
	return render(request, 'WeatherSTUFF/changedetails.html', context=context_dict)

def about(request):
	return render(request, 'WeatherSTUFF/about.html')

# Create new user account
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

			login(request, user)
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
				return redirect(reverse('WeatherSTUFF:myaccount'))
			else:
				return HttpResponse("Your account has been disabled.")
		else:
			return render(request, 'WeatherSTUFF/login.html', context={"message":"Invalid login details, please try again"})

	else:

		return render(request, 'WeatherSTUFF/login.html', context={})

@login_required
def user_logout(request):
	logout(request)
	return redirect(reverse('WeatherSTUFF:logged_out'))

def logged_out(request):
	return render(request, 'WeatherSTUFF/logout.html')

@login_required
def delete_account(request):

	if request.method == 'POST':

		if request.user.is_authenticated:
			form = DeleteProfileForm(request.POST)
			userProf = UserProfile.objects.filter(user__exact=request.user).first()
			userProf.delete()
			request.user.delete()

			return render(request, 'WeatherSTUFF/deleteaccount.html', context={"message":"Your account has been deleted", "form":form})
		else:
			return render(request, 'WeatherSTUFF/deleteaccount.html', context={"message":"Invaid details, could not delete account"})
	else:

		return render(request, 'WeatherSTUFF/deleteaccount.html')


# Receive a pin post request, save pin to server
def add_pin(request):
    if request.method == 'POST':
        datenow = datetime.datetime.now() # python wants the date in an exact format
        print("Request user:" + str(request.user))
        try:
            if(request.user.is_authenticated):
                userProf = UserProfile.objects.filter(user__exact=request.user).first()
            else:
                raise UserProfile.DoesNotExist
        except UserProfile.DoesNotExist:
            return HttpResponse(status=401, content="No User found, you are not logged in.")

        # If there is a pin in the same location and it is owned by the same user,
        # then update the pin currently at that location rather than creating a new one

        obj, created = Pin.objects.update_or_create(x_val = request.POST['lng'], y_val = request.POST['lat'], defaults={
        "user":userProf,
        "date":datenow,
        "x_val":request.POST['lng'],
        "y_val":request.POST['lat'],
        "title":request.POST['title'],
        "content":request.POST['content']
        })

        print(created)
        print(obj)
        #p = Pin(  \
        #user = userProf, \
        #date = datenow, \
        #x_val = request.POST['lng'], \
        #y_val = request.POST['lat'], \
        #title = request.POST['title'], \
        #content = request.POST['content'], \
        #)
        #p.save()
        return HttpResponse(status=201)

def get_pins(request):
    # Don't bother checking for anything, just
    # return a json of all the get_pins

    pin_data = serializers.serialize('json', Pin.objects.all())
    return HttpResponse(pin_data, content_type='application/json')

from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core import serializers
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse


import datetime

from WeatherSTUFF.models import Pin, UserProfile, FavouritePlace

#imports for user authentication
from WeatherSTUFF.forms import UserForm, UserProfileForm, DeleteProfileForm, DeletePinForm, FavPlaceForm
from django.contrib.auth.models import User#, DateTimeField
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.models import is_superuser
from django.contrib.auth.decorators import login_required
import math



#home page
def index(request):
	return render(request, 'WeatherSTUFF/index.html')


#about page
def about(request):
	return render(request, 'WeatherSTUFF/about.html')


# Create new user account
def sign_up(request):

	registered = False
	if request.method == 'POST':
		#get the forms
		user_form = UserForm(request.POST)
		profile_form = UserProfileForm(request.POST)

		#get the data input into the forms and save the details in a new object in the models
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit = False)
			profile.user = user

			if 'profile_picture' in request.FILES:
				profile.profile_picture = request.FILES['profile_picture']
			profile.save()

			registered = True

			login(request, user)
		else:
			print(user_form.errors, profile_form.errors)
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render(request, 'WeatherSTUFF/register.html', context = {'user_form':user_form, 'profile_form': profile_form, 'registered': registered})

#login page
def sign_in(request):

	if request.method == 'POST':
		#get the details entered into the form and authenticate them
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username = username, password = password)

		#if the details are correct, log the user in
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

#my account page
def my_account(request):
	#only give access if the user is authenticated
	if request.user.is_authenticated:
		#get the user profile, any pins that the user has placed and any favourite places that they have
		userProf = UserProfile.objects.filter(user__exact=request.user).first()
		pins = Pin.objects.filter(user=userProf)
		fav_places = FavouritePlace.objects.filter(user=userProf)

		#pass all the necessary details through the context dictionary
		return render(request, 'WeatherSTUFF/myaccount.html', context={'userProf':userProf, 'pins':pins, 'fav_places':fav_places})
	else:
		return render(request, 'WeatherSTUFF/myaccount.html')


# Edit an existing account
@login_required
def change_details(request):
	#get user profile of current user
	user_prof = UserProfile.objects.filter(user__exact=request.user).first()

	if request.method == 'POST':
		#get the forms, passing in the user's data to populate them
		user_form = UserForm(request.POST, instance=request.user)
		profile_form = UserProfileForm(request.POST, instance=user_prof)

		#get the data input into the forms and save the details in the object
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit = False)

			profile.user = user

			if 'profile_picture' in request.FILES:
				profile.profile_picture = request.FILES['profile_picture']
			profile.save()

			login(request, user)
			return redirect(reverse('WeatherSTUFF:myaccount'))
		else:
			print(user_form.errors, profile_form.errors)
	else:
		user_form = UserForm(instance=request.user)
		profile_form = UserProfileForm(instance=user_prof)

	return render(request, 'WeatherSTUFF/changedetails.html', context = {'user_form':user_form, 'profile_form': profile_form})


#delete the user account
@login_required
def delete_account(request):

	if request.method == 'POST':
		#only do if the user is logged in
		if request.user.is_authenticated:
			#get the form
			form = DeleteProfileForm(request.POST)
			#get the user profile
			userProf = UserProfile.objects.filter(user__exact=request.user).first()
			#delete the userProfile object and the user object
			userProf.delete()
			request.user.delete()

			return render(request, 'WeatherSTUFF/deleteaccount.html', context={"message":"Your account has been deleted", "form":form})
		else:
			return render(request, 'WeatherSTUFF/deleteaccount.html', context={"message":"Invaid details, could not delete account"})
	else:

		return render(request, 'WeatherSTUFF/deleteaccount.html')


#log the user out
@login_required
def user_logout(request):
	logout(request)
	return redirect(reverse('WeatherSTUFF:logged_out'))


#page user redirected to after logged out
def logged_out(request):
	return render(request, 'WeatherSTUFF/logout.html')


#add a favourite location
def add_fav(request):

	#get the profile associated with the user
	userProf = UserProfile.objects.filter(user__exact=request.user).first()

	form = FavPlaceForm()

	#process the form to add the favourite
	if request.method=="POST":
		form = FavPlaceForm(request.POST)
		if form.is_valid():
			fav_place = form.save(commit=False)
			#assign the current user profile to the user field of the fav_place object
			fav_place.user = userProf
			fav_place.save()
			#redirect the user to their myaccount page
			return redirect(reverse('WeatherSTUFF:myaccount'))

	return render(request, 'WeatherSTUFF/addfav.html', context={'form':form})


#show the details of their favourite location
def show_fav_place(request, fav_place_slug):

	#get the faovourite place
	fav_place = FavouritePlace.objects.filter(slug=fav_place_slug).first()
	form = FavPlaceForm()

	#get all the pins
	all_pins = Pin.objects.all()
	pins = []

	#check each pins, appending it to the list if it is close to our favourite location
	for pin in all_pins:
		diff_x = fav_place.x_val-pin.x_val
		diff_y = fav_place.x_val-pin.x_val
		distance = math.sqrt((diff_x**2)+(diff_y**2))
		if distance<10:
			pins.append(pin)

	#process the form to delete the favourite place
	#if button pressed, the favourite place object is deleted from the model
	if request.method=="POST":
		form = FavPlaceForm(request.POST)
		fav_place.delete()
		#redirect the user to their myaccount page
		return redirect(reverse('WeatherSTUFF:myaccount'))
	return render(request, 'WeatherSTUFF/favPlace.html', context={'form':form, 'fav_place':fav_place, 'pins':pins})

#show details of pin
def show_pin(request, pin_name_slug):

	#get the pin
	pin= Pin.objects.filter(slug=pin_name_slug).first()
	form = DeletePinForm()

	#process the form to delete the pin
	#if button pressed, the pin object is deleted
	if request.method=="POST":
		form = DeletePinForm(request.POST)
		pin.delete()
		#redirect the user to their myaccount page
		return redirect(reverse('WeatherSTUFF:myaccount'))
	return render(request, 'WeatherSTUFF/pin.html', context={'form':form, 'pin':pin})


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

        # Check if the Pin exists, and if it does, then check if this user owns it
        # or if the user if the admin
        qSet = Pin.objects.filter(x_val = request.POST['lng'], y_val = request.POST['lat'])
        if qSet.exists():
            p = qSet.first()
            if p != None:
                if (not request.user.is_superuser) and request.user.id != p.user.user.id:#str(userProf.user.username) != str(p.user.user.username):
                    return HttpResponse(status=401, content="That is not your pin to change.")

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

        # If the user posts this, then they must want this pin to be deleted
        if(obj.title == "DELETED" and obj.content == "DELETED"):
            obj.delete()
            return HttpResponse(status=200, content = "")
        #print("Edited")

        #print(created)
        #print(obj)
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

#get all the pins in the database
def get_pins(request):
    # Don't bother checking for anything, just
    # return a json of all the get_pins

    pin_data = serializers.serialize('json', Pin.objects.all(), use_natural_foreign_keys=True, use_natural_primary_keys=True, cls=LazyEncoder)
    #print(pin_data)
    return HttpResponse(pin_data, content_type='application/json')

# For the username rather than number
from django.core.serializers.json import DjangoJSONEncoder

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        print(obj.__str__())
        if isinstance(obj, datetime.datetime):
            return str(str(obj.date().day) +"/"+ str(obj.date().month) +"/"+ str(obj.date().year))
        return super().default(obj)

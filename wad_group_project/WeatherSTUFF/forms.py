
from django import forms
from WeatherSTUFF.models import UserProfile, Pin, FavouritePlace
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)

    class Meta:
            model = User
            fields = ('username', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture',)

class DeleteProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ()

class DeletePinForm(forms.ModelForm):
    class Meta:
        model = Pin
        fields = ()

class EditUserForm(forms.ModelForm):
    username = forms.CharField(required=True)
    password = forms.CharField(widget = forms.PasswordInput, required=True)
    class Meta:
        model=User
        fields = ('username', 'password',)

class FavPlaceForm(forms.ModelForm):
    class Meta:
        model=FavouritePlace
        fields = ('place_name', 'x_val', 'y_val',)







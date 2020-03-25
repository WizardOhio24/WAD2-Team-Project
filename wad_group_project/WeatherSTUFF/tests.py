from django.test import TestCase
from django.urls import reverse
from WeatherSTUFF.models import UserProfile, Pin, FavouritePlace
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
import pytz
import random


class PinMethodTests(TestCase):
    def test_ensure_num_ratings_are_positive(self):
        """
        Checks to make sure that the number of ratings for a Pin is non-zero.
        """
        user = generate_user()
        pin = generate_pin(user, num_ratings=-1)
        self.assertEqual((pin.num_ratings >= 0), True)

class IndexViewTests(TestCase):
    def test_index_view_with_no_pins(self):
        """
        If there are no pins, a message should be displayed
        """
        response = self.client.get(reverse('WeatherSTUFF:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no pins present.')

    def test_pins_display(self):
        user = generate_user()
        p1 = generate_pin(user = user, title="rain")
        p2 = generate_pin(user = user, title="fire")
        p3 = generate_pin(user = user, title="flood")

        response = self.client.get(reverse('WeatherSTUFF:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "rain")
        self.assertContains(response, "fire")
        self.assertContains(response, "flood")

class MyAccountViewTests(TestCase):
    def setUp(self):
        user = generate_user()
        self.client.force_login(User.objects.get_or_create(username='test')[0])

    def test_favourite_place_displays(self):
        """
        If user has a favourite place, should display on page
        """

        user = User.objects.get_or_create(username='test')[0]
        userprofile = UserProfile.objects.get_or_create(user=user)[0]
        place_name = "Glasgow"
        x_val = 0
        y_val = 0
        place = FavouritePlace(place_name=place_name, x_val=x_val, y_val=y_val, user=userprofile)
        place.save()

        response = self.client.get(reverse('WeatherSTUFF:myaccount'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Glasgow")
        


def generate_date():
    return datetime.datetime(year=random.randint(2010, 2020),
                             month=random.randint(1,12),
                             day=random.randint(1,28),
                             hour=random.randint(0,23),
                             minute=random.randint(0,59), 
                             tzinfo=pytz.UTC)

def generate_user(username="test", email="test@test.com", password="xxx"):
    t = User.objects.get_or_create(username=username,email=email,password=password)[0]
    s = UserProfile.objects.get_or_create(user=t)[0]
    s.save()
    return s

def generate_pin(user, num_ratings=0, rating=0, date=generate_date(), x_val=0, y_val=0, title="", content=""):
    pin = Pin(user=user, num_ratings = num_ratings, rating = rating, date=date, x_val=x_val, y_val=y_val)
    pin.save()
    return pin


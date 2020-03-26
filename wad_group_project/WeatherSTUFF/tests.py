import datetime
import json
import random
import time
import re

import pytest
import pytz
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase, TestCase
from django.urls import reverse
from django.utils import timezone

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from WeatherSTUFF.models import FavouritePlace, Pin, UserProfile


class SeleniumTests(StaticLiveServerTestCase):
    def setUp(self):
        User.objects.create_superuser(username='admin',
                                      password='admin',
                                      email='admin@example.com')

        self.driver = webdriver.Firefox()
        super(SeleniumTests, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(SeleniumTests, self).tearDown()

    def test_add_pin_while_not_signed_in(self):
        """
        Test to check that anonymous user cannot add a pin to the map
        """

        # Open index page
        self.driver.get(
            '%s%s' % (self.live_server_url, "/")
            )

        # Go through steps of adding a pin
        ac = ActionChains(self.driver)
        self.driver.set_window_size(550, 693)
        self.driver.find_element(By.CSS_SELECTOR, ".leaflet-draw-draw-marker").click()
        ac.move_to_element(self.driver.find_element(By.ID, "mapContainer")).move_by_offset(30, 30).click().perform()
        
        # Wait for an error message for upto 3 seconds
        for i in range(5):
            try:
                text = self.driver.switch_to.alert.text
                break
            except:
                time.sleep(0.5)

        # Either test alert for equality or fail if test times out
        try:
            self.assertEquals(text, "Error 401 : No User found, you are not logged in.")
        except:
            self.assertEqual(True, False)
        

    def test_create_user(self):
        """
        Django admin create user test
        Create a user in django admin and assert that
        page is redirected to new user change form.
        """

        # Open the django admin page

        
        self.driver.get(
            '%s%s' % (self.live_server_url, "/admin/")
        )

        # Fill login information of admin
        username = self.driver.find_element_by_id("id_username")
        username.send_keys("admin")
        password = self.driver.find_element_by_id("id_password")
        password.send_keys("admin")

        # Locate Login button and click it
        self.driver.find_element_by_xpath('//input[@value="Log in"]').click()
        self.driver.get(
            '%s%s' % (self.live_server_url, "/admin/auth/user/add/")
        )

        # Fill the create user form with username and password
        self.driver.find_element_by_id("id_username").send_keys("test")
        self.driver.find_element_by_id("id_password1").send_keys("test")
        self.driver.find_element_by_id("id_password2").send_keys("test")

        # Forms can be submitted directly by calling its method submit
        self.driver.find_element_by_id("user_form").submit()
        self.assertIn("Add user", self.driver.title)


class SignUpTests(StaticLiveServerTestCase):
    def setUp(self):
        User.objects.create_superuser(username='admin',
                                    password='admin',
                                    email='admin@example.com')

        self.driver = webdriver.Firefox()
        super(SignUpTests, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(SignUpTests, self).tearDown()

    def test_valid_sign_up(self):
        """
        Tests that a sign up results in a user being added to the database
        """

        # Get the register page
        self.driver.get(
            '%s%s' % (self.live_server_url, reverse("WeatherSTUFF:register"))
            )

        # Sign up with a new user 'test'
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys("test")
        self.driver.find_element(By.ID, "id_password").click()
        self.driver.find_element(By.ID, "id_password").send_keys("test123")
        self.driver.find_element(By.ID, "registerButton").click()

        # Check that new user added to database sucessfully
        try:
            user = User.objects.get(username='test')
            self.assertIsNotNone(user)
        except:
            self.assertFalse(True)
    

    def test_sign_up_user_already_exists(self):
        """
        Tests that trying to sign up with a username which is already taken 
        results in a message being displayed
        """
        user = generate_user(username="bobby")

        # Get the register page
        self.driver.get(
            '%s%s' % (self.live_server_url, reverse("WeatherSTUFF:register"))
            )

        # Sign up with a new user 'test'
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys("bobby")
        self.driver.find_element(By.ID, "id_password").click()
        self.driver.find_element(By.ID, "id_password").send_keys("test123")
        self.driver.find_element(By.ID, "registerButton").click()

        src = self.driver.page_source
        text_found = re.search(r'A user with that username already exists.', src)
        self.assertNotEqual(text_found, None)


class SignInTests(StaticLiveServerTestCase):
    def setUp(self):
        User.objects.create_superuser(username='admin',
                                    password='admin',
                                    email='admin@example.com')

        self.driver = webdriver.Firefox()
        super(SignInTests, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(SignInTests, self).tearDown()
    
        
    def test_invalid_sign_in_credentials(self):
        """
        Tests that a sign up results in a user being added to the database
        """

        # Get the register page
        self.driver.get(
            '%s%s' % (self.live_server_url, reverse("WeatherSTUFF:login"))
            )

        # Sign up with a new user 'test'
        self.driver.find_element(By.NAME, "username").send_keys("unknownuser")
        self.driver.find_element(By.NAME, "password").send_keys("unknown")
        self.driver.find_element(By.ID, "loginButton").click()

        src = self.driver.page_source
        text_found = re.search(r'Invalid login details, please try again', src)
        self.assertNotEqual(text_found, None)

    def test_valid_sign_in_credentials(self):
        """
        Tests that a sign up results in a user being added to the database
        """

        # Get the register page
        self.driver.get(
            '%s%s' % (self.live_server_url, reverse("WeatherSTUFF:login"))
            )

        # Sign up with a new user 'test'
        self.driver.find_element(By.NAME, "username").send_keys("admin")
        self.driver.find_element(By.NAME, "password").send_keys("admin")
        self.driver.find_element(By.ID, "loginButton").click()

        url = self.driver.current_url
        my_account_url = '%s%s' % (self.live_server_url, reverse("WeatherSTUFF:myaccount"))
        self.assertEquals(url, my_account_url)



class PinMethodTests(TestCase):
    def test_ensure_num_ratings_are_positive(self):
        """
        Checks to make sure that the number of ratings for a Pin is non-zero.
        """
        user = generate_user()
        pin = generate_pin(user, num_ratings=-1)
        self.assertEqual((pin.num_ratings >= 0), True)


class AboutViewTests(TestCase):
    def test_about_content_displays(self):
        """
        Check that about page displays correctly
        """
        response = self.client.get(reverse('WeatherSTUFF:about'))
        self.assertEqual(response.status_code, 200)
        text = "We are a group of university students" 
        self.assertContains(response, text)


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

    def test_user_pins_displays(self):
        pass

    def test_logout(self):
        pass


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

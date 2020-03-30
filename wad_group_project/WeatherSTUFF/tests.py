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
from WeatherSTUFF.forms import UserForm, UserProfileForm, DeleteProfileForm, DeletePinForm, FavPlaceForm
from populate import populate


class PinMethodTests(TestCase):
    def test_ensure_num_ratings_are_positive(self):
        """
        Checks to make sure that the number of ratings for a Pin is non-zero.
        """
        user = generate_user()
        pin = generate_pin(user, num_ratings=-1)
        self.assertEqual((pin.num_ratings >= 0), True)

    def test_valid_pin(self):
        """
        Checks that a valid pin is added sucessfully
        """
        user = generate_user()
        date = generate_date()
        pin = generate_pin(user = user,
                           date = date,
                           title = "testtitle",
                           content = "testcontent",
                           rating = 5,
                           num_ratings = 10,
                           x_val = 0,
                           y_val = 50)

        self.assertEqual(pin.user, user)
        self.assertEqual(pin.date, date)
        self.assertEqual(pin.title, "testtitle")
        self.assertEqual(pin.content, "testcontent")
        self.assertEqual(pin.rating, 5)
        self.assertEqual(pin.num_ratings, 10)
        self.assertEqual(pin.x_val, 0)
        self.assertEqual(pin.y_val, 50)

    def test_pin_to_string(self):
        """
        Checks to make sure that correct string is returned
        """
        user = generate_user()
        pin = generate_pin(user, title="test")
        self.assertEqual(str(pin), "test")

    def test_change_title(self):
        """
        Checks that pin title changes are reflected
        """
        user = generate_user()
        pin = generate_pin(user=user, title="test")
        pin.title = "newtest"
        pin.save()
        self.assertEqual(pin.title, "newtest")
    
    def test_change_content(self):
        """
        Checks that pin content changes are reflected
        """
        user = generate_user()
        pin = generate_pin(user=user, content="test")
        pin.content = "newtest"
        pin.save()
        self.assertEqual(pin.content, "newtest")

    def test_change_x_val(self):
        """
        Checks that pin x_val changes are reflected
        """
        user = generate_user()
        pin = generate_pin(user=user, x_val=0)
        pin.x_val = 1
        pin.save()
        self.assertEqual(pin.x_val, 1)
    
    def test_change_y_val(self):
        """
        Checks that pin y_val changes are reflected
        """
        user = generate_user()
        pin = generate_pin(user=user, y_val=0)
        pin.y_val = 1
        pin.save()
        self.assertEqual(pin.y_val, 1)

    def test_change_date(self):
        """
        Checks that pin date changes are reflected
        """
        user = generate_user()
        pin = generate_pin(user=user)
        date = generate_date()
        pin.date = date
        pin.save()
        self.assertEqual(pin.date, date)

    def test_change_rating(self):
        """
        Checks that pin rating changes are reflected
        """
        user = generate_user()
        pin = generate_pin(user=user, rating=10)
        pin.rating = 11
        pin.save()
        self.assertEqual(pin.rating, 11)

    def test_change_num_ratings(self):
        """
        Checks that pin num_ratings changes are reflected
        """
        user = generate_user()
        pin = generate_pin(user=user, num_ratings = 10)
        pin.num_ratings = 11
        pin.save()
        self.assertEqual(pin.num_ratings, 11)


class UserProfileMethodTests(TestCase):
    def test_ensure_pins_delete_on_user_delete(self):
        """
        Checks to make sure that the number of ratings for a Pin is non-zero.
        """
        user = generate_user()
        pin1 = generate_pin(user, title="test1")
        pin2 = generate_pin(user, title="test2")
        pin3 = generate_pin(user, title="test3")
        user.delete()

        pins = Pin.objects.filter(user=user)
        self.assertEqual(pins.count(), 0)

    def test_user_profile_to_string(self):
        """
        Checks to make sure that correct string is returned
        """
        user = generate_user(username="tester")
        
        self.assertEqual(str(user), "tester")

    def test_valid_user(self):
        """
        Checks that a valid user is added sucessfully
        """
        user = generate_user(username='test',
                             email = "test@test.com",
                             password = "test")

        self.assertEqual(user.user.username, 'test')
        self.assertEqual(user.user.email, 'test@test.com')
        self.assertEqual(user.user.password, 'test')

    def test_add_pin_to_user(self):
        """
        Checks that pins can be added to user profiles
        """
        user = generate_user()
        pin = generate_pin(user)
        pins = Pin.objects.filter(user=user)
        self.assertEqual(pins.count(), 1)

    def test_add_favourite_place_to_user(self):
        """
        Checks that favourite places can be added to user profiles
        """
        user = generate_user()
        place = generate_favourite_place(user)
        places = FavouritePlace.objects.filter(user=user)
        self.assertEqual(places.count(), 1)


class FavouritePlaceMethodTests(TestCase):
    def test_favourite_place_to_string(self):
        """
        Checks to make sure that correct string is returned
        """
        user = generate_user()
        place = generate_favourite_place(user, place_name="test")
        self.assertEqual(str(place), "test")

    def test_valid_favourite_place(self):
        """
        Checks that a valid favourite place can be added
        """
        user = generate_user()
        place = generate_favourite_place(user = user,
                                         place_name = "test",
                                         x_val = 0,
                                         y_val = 10)

        self.assertEqual(place.user, user)
        self.assertEqual(place.place_name, "test")
        self.assertEqual(place.x_val, 0)
        self.assertEqual(place.y_val, 10)

class PopulateScriptTest(TestCase):
    def test_populate_users(self):
        """
        Checks that users populate correctly
        """
        populate()
        users = UserProfile.objects.all()
        self.assertEquals(users.count(), 4)

    def test_populate_pins(self):
        """
        Checks that pins populate properly
        """
        populate()
        pins = Pin.objects.all()
        self.assertEquals(pins.count(), 11)

    def test_populate_favourite_places(self):
        """
        Checks favourite place populates correctly
        """
        populate()
        places = FavouritePlace.objects.all()
        self.assertEquals(places.count(), 5)
        

class FormTests(TestCase):
    def test_user_form(self):
        """
        Tests user form is valid
        """
        form_data = {'username': 'test', 'password': 'test'}
        form = UserForm(form_data)
        self.assertTrue(form.is_valid())

    def test_fav_place_form(self):
        """
        Tests favourite place form is valid
        """
        form_data = {'place_name': 'test', 'x_val': 0, 'y_val': 0}
        form = FavPlaceForm(form_data)
        self.assertTrue(form.is_valid())

    def test_user_profile_form(self):
        """
        Tests user profile form is valid
        """
        form_data = {'profile_picture': None}
        form = UserProfileForm(form_data)
        self.assertTrue(form.is_valid())
    
    def test_user_delete_form(self):
        """
        Tests user delete form is valid
        """
        form_data = {}
        form = DeleteProfileForm(form_data)
        self.assertTrue(form.is_valid())

    def test_delete_pin_form(self):
        """
        Tests delete pin form is valid
        """
        form_data = {}
        form = DeletePinForm(self)
        self.assertTrue(form.is_valid())


class MapTests(StaticLiveServerTestCase):
    def setUp(self):
        User.objects.create_superuser(username='admin',
                                      password='admin',
                                      email='admin@example.com')

        self.driver = webdriver.Firefox()
        super(MapTests, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(MapTests, self).tearDown()

    def test_add_pin_while_not_signed_in(self):
        """
        Test to check that anonymous user cannot add a pin to the map
        """

        # Open index page
        self.driver.get(
            '%s%s' % (self.live_server_url, "/")
            )

        time.sleep(10)

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
            assert False

    def test_edit_pin_not_signed_in(self):
        """
        Test to check that anonymous user cannot edit a pin on the map
        """
        user = generate_user()
        pin = generate_pin(user = user, title = "TEST", content = "TEST")

        # Open index page
        self.driver.get(
            '%s%s' % (self.live_server_url, "/")
            )

        # Go through steps of adding a pin
        ac = ActionChains(self.driver)
        self.driver.set_window_size(550, 693)
        self.driver.find_element(By.CSS_SELECTOR, ".leaflet-marker-icon:nth-child(1)").click()
        self.driver.find_element(By.LINK_TEXT, "Edit").click()
        element = self.driver.find_element(By.CSS_SELECTOR, ".leaflet-popup-input:nth-child(1)")
        self.driver.execute_script("if(arguments[0].contentEditable === 'true') {arguments[0].innerText = 'Edited'}", element)
        element = self.driver.find_element(By.CSS_SELECTOR, ".leaflet-popup-input:nth-child(2)")
        self.driver.execute_script("if(arguments[0].contentEditable === 'true') {arguments[0].innerText = 'Edited'}", element)
        self.driver.find_element(By.LINK_TEXT, "Save").click()

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
            assert False

    def test_add_pin_signed_in(self):
        """
        Test to check that a signed in user can add a pin to the map
        """

        # Open signup page
        self.driver.get(
            '%s%s' % (self.live_server_url, reverse("WeatherSTUFF:register"))
            )

        # Go through steps of signing up
        ac = ActionChains(self.driver)
        self.driver.set_window_size(550, 693)
        self.driver.find_element(By.ID, "id_username").send_keys("test")
        self.driver.find_element(By.ID, "id_password").send_keys("test")
        self.driver.find_element(By.ID, "registerButton").click()
        self.driver.find_element(By.LINK_TEXT, "Home").click()

        # GO through steps of adding a pin
        self.driver.find_element(By.CSS_SELECTOR, ".leaflet-draw-draw-marker").click()
        ac.move_to_element(self.driver.find_element(By.ID, "mapContainer")).move_by_offset(30, 30).click().perform()
        self.driver.find_element(By.CSS_SELECTOR, ".leaflet-marker-icon:nth-child(1)").click()
        #time.sleep(0.2)

        # Check database for pins by the test user, wheck that pin has regestered
        user = User.objects.get(username="test")
        userProf = UserProfile.objects.get(user=user)
        pin = Pin.objects.filter(user=userProf)

        # Check that the user has added first pin to account
        self.assertEqual(pin.count(), 1)
        
    def test_delete_user_pin(self):
        """
        Test to check that a signed in user can delete their pins from map
        """

        # Open signup page
        self.driver.get(
            '%s%s' % (self.live_server_url, reverse("WeatherSTUFF:register"))
            )

        # Go through steps of signing up
        ac = ActionChains(self.driver)
        self.driver.set_window_size(550, 693)
        self.driver.find_element(By.ID, "id_username").send_keys("test")
        self.driver.find_element(By.ID, "id_password").send_keys("test")
        self.driver.find_element(By.ID, "registerButton").click()
        self.driver.find_element(By.LINK_TEXT, "Home").click()

        # Go through steps of adding a pin
        self.driver.find_element(By.CSS_SELECTOR, ".leaflet-draw-draw-marker").click()
        ac.move_to_element(self.driver.find_element(By.ID, "mapContainer")).move_by_offset(30, 30).click().perform()
        self.driver.find_element(By.CSS_SELECTOR, ".leaflet-marker-icon:nth-child(1)").click()

        # Delete the pin
        self.driver.find_element(By.CSS_SELECTOR, ".leaflet-draw-edit-remove").click()
        self.driver.find_element(By.CSS_SELECTOR, ".leaflet-marker-icon:nth-child(1)").click()
        time.sleep(0.2)

        # Check element is missing from map
        try:
            self.driver.find_element(By.CSS_SELECTOR, ".leaflet-marker-icon:nth-child(1)")
            assert False
        except:
            assert True

        # Below is a test to check that the pin was deleted from database
        """
        # Check database for pins by the test user, wheck that pin has regestered
        user = User.objects.get(username="test")
        userProf = UserProfile.objects.get(user=user)
        pin = Pin.objects.filter(user=userProf)

        # Check that the user has added first pin to account
        self.assertEqual(pin.count(), 0)
        """

    def test_edit_user_pin(self):
        """
        Test to check that a signed in user can edit their 
        own pin on the map
        """

        # Open signup page
        self.driver.get(
            '%s%s' % (self.live_server_url, reverse("WeatherSTUFF:register"))
            )

        # Go through steps of signing up
        ac = ActionChains(self.driver)
        self.driver.set_window_size(550, 693)
        self.driver.find_element(By.ID, "id_username").send_keys("test")
        self.driver.find_element(By.ID, "id_password").send_keys("test")
        self.driver.find_element(By.ID, "registerButton").click()
        self.driver.find_element(By.LINK_TEXT, "Home").click()

        # GO through steps of adding a pin
        self.driver.find_element(By.CSS_SELECTOR, ".leaflet-draw-draw-marker").click()
        ac.move_to_element(self.driver.find_element(By.ID, "mapContainer")).move_by_offset(30, 30).click().perform()
        self.driver.find_element(By.CSS_SELECTOR, ".leaflet-marker-icon:nth-child(1)").click()
        self.driver.find_element(By.LINK_TEXT, "Edit").click()
        element = self.driver.find_element(By.CSS_SELECTOR, ".leaflet-popup-input:nth-child(1)")
        self.driver.execute_script("if(arguments[0].contentEditable === 'true') {arguments[0].innerText = 'Edited'}", element)
        element = self.driver.find_element(By.CSS_SELECTOR, ".leaflet-popup-input:nth-child(2)")
        self.driver.execute_script("if(arguments[0].contentEditable === 'true') {arguments[0].innerText = 'Edited'}", element)
        self.driver.find_element(By.LINK_TEXT, "Save").click()
        self.driver.find_element(By.CSS_SELECTOR, ".leaflet-marker-icon:nth-child(1)").click()
        #time.sleep(0.2)

        # Check database for pins by the test user, wheck that pin has regestered
        user = User.objects.get(username="test")
        userProf = UserProfile.objects.get(user=user)
        pin = Pin.objects.filter(user=userProf)

        # Check that the user has added first pin to account
        self.assertEqual(str(pin[0]), "Edited")

    def test_edit_non_user_pin(self):
        """
        Test to check that users can't edit each others pins
        """
        user = generate_user(username="bob")
        pin = generate_pin(user = user, title = "TEST", content = "TEST")

        # Open signup page
        self.driver.get(
            '%s%s' % (self.live_server_url, reverse("WeatherSTUFF:register"))
            )

        # Go through steps of signing up
        ac = ActionChains(self.driver)
        self.driver.set_window_size(550, 693)
        self.driver.find_element(By.ID, "id_username").send_keys("test")
        self.driver.find_element(By.ID, "id_password").send_keys("test")
        self.driver.find_element(By.ID, "registerButton").click()
        self.driver.find_element(By.LINK_TEXT, "Home").click()

        # Go through steps of adding a pin
        ac = ActionChains(self.driver)
        self.driver.set_window_size(550, 693)
        self.driver.find_element(By.CSS_SELECTOR, ".leaflet-marker-icon:nth-child(1)").click()
        self.driver.find_element(By.LINK_TEXT, "Edit").click()
        element = self.driver.find_element(By.CSS_SELECTOR, ".leaflet-popup-input:nth-child(1)")
        self.driver.execute_script("if(arguments[0].contentEditable === 'true') {arguments[0].innerText = 'Edited'}", element)
        element = self.driver.find_element(By.CSS_SELECTOR, ".leaflet-popup-input:nth-child(2)")
        self.driver.execute_script("if(arguments[0].contentEditable === 'true') {arguments[0].innerText = 'Edited'}", element)
        self.driver.find_element(By.LINK_TEXT, "Save").click()

        # Wait for an error message for upto 3 seconds
        for i in range(5):
            try:
                text = self.driver.switch_to.alert.text
                break
            except:
                time.sleep(0.5)

        # Either test alert for equality or fail if test times out
        try:
            self.assertEquals(text, "Error 401 : That is not your pin to change.")
        except:
            assert False


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

        # Check error message is displayed
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
        Tests that a sign in with wrong details displays an error
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
        Tests that a sucessful sign in redirects to my account page
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

    def test_favourite_place_displays(self):
        """
        If user has a favourite place, should display on page
        """
        user = generate_user()
        self.client.force_login(User.objects.get_or_create(username='test')[0])
        place_name = "Glasgow"
        x_val = 0
        y_val = 0
        place = FavouritePlace(place_name=place_name, x_val=x_val, y_val=y_val, user=user)
        place.save()

        response = self.client.get(reverse('WeatherSTUFF:myaccount'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Glasgow")

    def test_user_pins_display(self):
        """
        If user has pins, should display on page
        """
        user = generate_user()
        self.client.force_login(User.objects.get_or_create(username='test')[0])
        pin = generate_pin(user=user, title="TESTDATATITLE", content="TESTDATACONTENT")
        response = self.client.get(reverse('WeatherSTUFF:myaccount'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TESTDATATITLE")
        self.assertContains(response, "TESTDATACONTENT")

    def test_links_for_anon_user(self):
        """
        If user is not signed in, should display links to sign up/sign in
        """
        response = self.client.get(reverse('WeatherSTUFF:myaccount'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign In")
        self.assertContains(response, "Sign Up")


class MyAccountSeleniumTests(StaticLiveServerTestCase):
    def setUp(self):
        User.objects.create_superuser(username='admin',
                                    password='admin',
                                    email='admin@example.com')

        self.driver = webdriver.Firefox()
        super(MyAccountSeleniumTests, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(MyAccountSeleniumTests, self).tearDown()

    def test_delete_user_account(self):
        """
        Test that a users deleted account is permenantly removed from database
        """

        # Open signup page
        self.driver.get(
            '%s%s' % (self.live_server_url, reverse("WeatherSTUFF:register"))
            )

        # Go through steps of signing up
        ac = ActionChains(self.driver)
        self.driver.set_window_size(550, 693)
        self.driver.find_element(By.ID, "id_username").send_keys("test")
        self.driver.find_element(By.ID, "id_password").send_keys("test")
        self.driver.find_element(By.ID, "registerButton").click()

        # Go through steps of deleting account
        self.driver.find_element(By.LINK_TEXT, "My Account").click()
        self.driver.find_element(By.ID, "accountButton").click()
        self.driver.find_element(By.ID, "deleteButton").click()

        # Check that user has been deleted from database
        try:
            user = User.objects.get(username="test")
            assert False
        except User.DoesNotExist:
            assert True

    def test_change_user_account_details(self):
        """
        Tests that when a user changes details on site the
        changes are reflected in the database
        """

        # Open signup page
        self.driver.get(
            '%s%s' % (self.live_server_url, reverse("WeatherSTUFF:register"))
            )

        # Go through steps of signing up
        ac = ActionChains(self.driver)
        self.driver.set_window_size(550, 693)
        self.driver.find_element(By.ID, "id_username").send_keys("test")
        self.driver.find_element(By.ID, "id_password").send_keys("test")
        self.driver.find_element(By.ID, "registerButton").click()

        # Go through steps of changing details
        self.driver.find_element(By.LINK_TEXT, "My Account").click()
        self.driver.find_element(By.LINK_TEXT, "Change Details").click()
        self.driver.find_element(By.ID, "id_username").clear()
        self.driver.find_element(By.ID, "id_username").send_keys("newtest")
        self.driver.find_element(By.ID, "id_password").clear()
        self.driver.find_element(By.ID, "id_password").send_keys("newtest")
        self.driver.find_element(By.ID, "updateButton").click()
        
        # Check that username has changed sucessfully
        try:
            user = User.objects.get(username="newtest")
            # Check that old username no longer exists
            try:
                old_user = User.objects.get(username="test")
                assert False
            except User.DoesNotExist:
                assert True   
        except User.DoesNotExist:
            assert False


def generate_date():
    """
    Helper method to generate date
    """
    return datetime.datetime(year=random.randint(2010, 2020),
                             month=random.randint(1,12),
                             day=random.randint(1,28),
                             hour=random.randint(0,23),
                             minute=random.randint(0,59), 
                             tzinfo=pytz.UTC)

def generate_user(username="test", email="test@test.com", password="xxx"):
    """
    Helper method to generate user profile
    """
    t = User.objects.get_or_create(username=username,email=email,password=password)[0]
    s = UserProfile.objects.get_or_create(user=t)[0]
    s.save()
    return s

def generate_pin(user, num_ratings=0, rating=0, date=generate_date(), x_val=0, y_val=0, title="", content=""):
    """
    Helper method to generate pins
    """
    pin = Pin(user=user, num_ratings = num_ratings, rating = rating, date=date, x_val=x_val, y_val=y_val)
    pin.title = title
    pin.content = content
    pin.save()
    return pin

def generate_favourite_place(user, place_name="none", x_val=0, y_val=0):
    """
    Helper method to generate favourite place
    """
    p = FavouritePlace(user=user, place_name=place_name, x_val=x_val, y_val=y_val)
    p.save()
    return p
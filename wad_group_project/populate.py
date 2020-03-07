import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'wad_group_project.settings')

import django
django.setup()

import datetime
from django.utils import timezone
import pytz
from WeatherSTUFF.models import UserProfile, Pin
from django.contrib.auth.models import User
import random
from django.db import IntegrityError

DUMMY_PASSWORD = "XXX"

def populate():

    user_A_pins = [
        {'title': 'STORM HERE!',
         'content': 'Storm Larry is passing through this area today.',
         'date': generate_date(),
         'rating': 18,
         'num_ratings':7,
         'x_val': 30.4999,
         'y_val': -53.0234,
         },
        {'title': 'flooded street, traffic diverted!!',
         'content': 'cars are being diverted via the A83',
         'date': generate_date(),
         'rating': 0,
         'num_ratings':0,
         'x_val': 34.4999,
         'y_val': -49.0234,
        }
    ]

    user_B_pins = [
        {'title': 'I dont know',
         'content': 'how this map works :(',
         'date': generate_date(),
         'rating': -8,
         'num_ratings':20,
         'x_val': 120.4999,
         'y_val': -23.0234,
         },
    ]

    user_C_pins = [
        {'title': 'Bushfires in this area',
         'content': 'Have been spreading for 4 days, this area is high risk!',
         'date': generate_date(),
         'rating': 24,
         'num_ratings':30,
         'x_val': 100.4999,
         'y_val': 3.0234,
         },
        {'title': 'Heavy rainfall expected',
         'content': 'reports of high rains, possible flooding',
         'date': generate_date(),
         'rating': 4,
         'num_ratings':12,
         'x_val': 99.4999,
         'y_val': 2.0234,
         },
    ]

    user_D_pins = [
        {'title': 'Road reopened here',
         'content': 'The road that was closed because of a blown down tree has reopened',
         'date': generate_date(),
         'rating': -8,
         'num_ratings':20,
         'x_val': 20.4999,
         'y_val': -73.0234,
         },
    ]

    users = {'richard': {'pins': user_A_pins, 'f_name': 'Richard', 'l_name': 'Menzies', 'email': 'richard@menzies.com'},
             'kieran': {'pins': user_B_pins, 'f_name': 'Kieran', 'l_name': 'Grant', 'email': 'kieran@grant.org'},
             'david': {'pins': user_C_pins, 'f_name': 'David', 'l_name': 'O\'Neill', 'email': 'david@oneill.gov'},
             'mia': {'pins': user_D_pins, 'f_name': 'Mia', 'l_name': 'Stevenson', 'email': 'mia@stevenson.co.uk'}
    }

    # The code below goes through the users dictionary, then adds each category, 
    # and then adds all the associated pages for that category.

    for user, user_data in users.items():
        u = add_user(user, user_data)
        for p in user_data['pins']:
            add_pin(u, p)

    for c in UserProfile.objects.all():
        for p in Pin.objects.filter(user = c):
            print(f' - {c}: {p}')

def add_user(user, user_data):
    f_name = user_data['f_name']
    l_name = user_data['l_name']
    email = user_data['email']

    t = User.objects.get_or_create(username=user,email=email,password=DUMMY_PASSWORD)[0]
    s = UserProfile.objects.get_or_create(user=t)[0]
    s.save()
    return s



def add_pin(u, data):
    p = Pin.objects.get_or_create(user=u,
                                  date=data['date'],
                                  x_val=data['x_val'],
                                  y_val=data['y_val'], 
                                  title=data['title'], 
                                  content=data['content'])[0]

    p.rating = data['rating']
    p.num_ratings = data['num_ratings']

    p.save()
    return p

def generate_date():
    return datetime.datetime(year=random.randint(2010, 2020),
                             month=random.randint(1,12),
                             day=random.randint(1,28),
                             hour=random.randint(0,23),
                             minute=random.randint(0,59), 
                             tzinfo=pytz.UTC)

    
if __name__ == '__main__':
    print("Starting WeatherSTUFF population script...")
    populate()
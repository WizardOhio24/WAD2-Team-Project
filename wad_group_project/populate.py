import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'wad_group_project.settings')

import django
django.setup()

import datetime
from django.utils import timezone
import pytz
from WeatherSTUFF.models import UserProfile, Pin, FavouritePlace
from django.contrib.auth.models import User
import random
from django.db import IntegrityError

DUMMY_PASSWORD = "XXX"

# AT THE MOMENT:
# x_val = latitude
# y_val = longitude

def populate():

    user_A_pins = [
        {'title': 'STORM HERE!',
         'content': 'Storm Larry is passing through this area today.',
         'date': generate_date(),
         'rating': 18,
         'num_ratings':23,
         'x_val': -3.605120,
         'y_val': 55.070858,
         },
        {'title': 'flooded street, traffic diverted!!',
         'content': 'cars are being diverted via the A83',
         'date': generate_date(),
         'rating': 3,
         'num_ratings':4,
         'x_val': -4.948221,
         'y_val': 56.217726,
        },
        {'title': 'Tornado Warning',
         'content': 'Winds of upto 130mph in the worst case.',
         'date': generate_date(),
         'rating': 43,
         'num_ratings':37,
         'x_val': -98.484245,
         'y_val': 39.011902,
         },
        {'title': 'No longer able to access via frozen river',
         'content': 'Warm weather has caused rapidly melting ice, no longer safe to traverse',
         'date': generate_date(),
         'rating': 17,
         'num_ratings':13,
         'x_val': 129.675476,
         'y_val': 62.035454,
        },
    ]

    user_B_pins = [
        {'title': 'I dont know',
         'content': 'how this map works :(',
         'date': generate_date(),
         'rating': -20,
         'num_ratings':20,
         'x_val': -32.311486,
         'y_val': 35.690206,
         },
         {'title': 'VOLCANIC ERUPTION',
         'content': 'Large parts of city have been destoryed :(',
         'date': generate_date(),
         'rating': -47,
         'num_ratings':100,
         'x_val': 14.498059,
         'y_val': 40.745448,
         },
    ]

    user_C_pins = [
        {'title': 'Bushfires in this area',
         'content': 'Have been spreading for 4 days, this area is high risk!',
         'date': generate_date(),
         'rating': 24,
         'num_ratings':30,
         'x_val': 150.981930,
         'y_val': -33.403931,
         },
        {'title': 'Heavy rainfall expected',
         'content': 'reports of high rains, possible flooding',
         'date': generate_date(),
         'rating': 4,
         'num_ratings':12,
         'x_val': 18.454794,
         'y_val': -33.737349,
         },
        {'title': 'Mudslide',
         'content': 'Road blocked, traffic diverted',
         'date': generate_date(),
         'rating': 20,
         'num_ratings':13,
         'x_val': -55.217760,
         'y_val': -7.969237,
         },
        {'title': 'Typhoon warning, flights cancelled',
         'content': 'reports of high winds, cautionary measures should be taken',
         'date': generate_date(),
         'rating': 4,
         'num_ratings':12,
         'x_val': 124.924903,
         'y_val': 1.545619,
         },
         
    ]

    user_D_pins = [
        {'title': 'Road reopened here',
         'content': 'The road that was closed because of a blown down tree has reopened',
         'date': generate_date(),
         'rating': -8,
         'num_ratings':20,
         'x_val': 13.830021,
         'y_val': 52.141750,
         },
    ]

    user_A_favourite_places = [
        {'place_name': 'Glasgow',
         'x_val': -3.605120,
         'y_val': 55.070858,
        },
        {'place_name': 'Ardno',
         'x_val': -4.948221,
         'y_val': 56.217726,
        },
    ]

    user_B_favourite_places = [
         {'place_name': 'Pompeii',
         'x_val': 14.498059,
         'y_val': 40.745448,
         },
    ]

    user_C_favourite_places = [
        {'place_name': 'Sydney',
         'x_val': 150.981930,
         'y_val': -33.403931,
         },
    ]

    user_D_favourite_places = [
        {'place_name': 'Berlin',
         'x_val': 13.830021,
         'y_val': 52.141750,
         },
    ]

    users = {'richard': {'pins': user_A_pins, 'favourite_places': user_A_favourite_places,'f_name': 'Richard', 'l_name': 'Menzies', 'email': 'richard@menzies.com'},
             'kieran': {'pins': user_B_pins, 'favourite_places': user_B_favourite_places,'f_name': 'Kieran', 'l_name': 'Grant', 'email': 'kieran@grant.org'},
             'david': {'pins': user_C_pins, 'favourite_places': user_C_favourite_places,'f_name': 'David', 'l_name': 'O\'Neill', 'email': 'david@oneill.gov'},
             'mia': {'pins': user_D_pins, 'favourite_places': user_D_favourite_places,'f_name': 'Mia', 'l_name': 'Stevenson', 'email': 'mia@stevenson.co.uk'}
    }

    # The code below goes through the users dictionary, then adds each category, 
    # and then adds all the associated pages for that category.

    for user, user_data in users.items():
        u = add_user(user, user_data)
        for p in user_data['pins']:
            add_pin(u, p)

        for l in user_data['favourite_places']:
            add_favourite_place(u, l)

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

def add_favourite_place(u, data):
    f = FavouritePlace.objects.get_or_create(user=u,
                                             place_name=data['place_name'],
                                             x_val=data['x_val'],
                                             y_val=data['y_val'])[0]
    f.save()
    return f

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
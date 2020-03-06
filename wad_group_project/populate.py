import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'wad_group_project.settings')

import django
django.setup()

import datetime
from django.utils import timezone
import pytz
from WeatherSTUFF.models import UserProfile, Pin
import random

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

    users = {'Richard': {'pins': user_A_pins},
             'Kieran': {'pins': user_B_pins},
             'David': {'pins': user_C_pins},
             'Mia': {'pins': user_D_pins}
    }

    # The code below goes through the users dictionary, then adds each category, 
    # and then adds all the associated pages for that category.

    for user, user_data in users.items():
        u = add_user(user)
        for p in user_data['pins']:
            add_pin(u, p)

    for c in UserProfile.objects.all():
        for p in Pin.objects.filter(user = c):
            print(f' - {c}: {p}')

def add_user(user):
    u = UserProfile.objects.get_or_create(username=user)[0]
    u.save()
    return u

def add_pin(u, data):
    d = data['date']
    x = data['x_val']
    y = data['y_val']
    t = data['title']
    c = data['content']
    p = Pin.objects.get_or_create(user=u,date=d,x_val=x,y_val=y, title=t, content=c)[0]
    p.rating = data['rating']
    p.num_ratings = data['num_ratings']

    p.save()
    return p

def generate_date():
    y = random.randint(2010, 2020)
    m = random.randint(1,11)
    d = random.randint(1,28)
    h= random.randint(0,23) 
    m= random.randint(0,59)
    tz= pytz.UTC
    return datetime.datetime(year=y,month=random.randint(1,12),day=d,hour=h,minute=m, tzinfo=tz)

    
if __name__ == '__main__':
    print("Starting WeatherSTUFF population script...")
    populate()
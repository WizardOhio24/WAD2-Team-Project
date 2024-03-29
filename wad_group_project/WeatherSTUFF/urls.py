from django.urls import path
from WeatherSTUFF import views


app_name = 'WeatherSTUFF'

urlpatterns = [ path('', views.index, name='index'),
                path('about/', views.about, name='about'),
                path('login/', views.sign_in, name='login'),
                path('register/', views.sign_up, name='register'),
                path('login/myaccount/', views.my_account, name='myaccount'),
                path('login/myaccount/changedetails/', views.change_details, name='changedetails'),
                path('login/myaccount/deleteaccount/', views.delete_account, name='deleteaccount'),
                path('logout/', views.user_logout, name = 'logout'),
                path('add_pin/', views.add_pin, name='add_pin'),
                path('get_pins/', views.get_pins, name='get_pins'),
                path('login/myaccount//<slug:pin_name_slug>/', views.show_pin, name='show_pin'),
                path('logout', views.logged_out, name='logged_out'),
                path('login/myaccount/addfav', views.add_fav, name='add_fav'),
                path('login/myaccount/<slug:fav_place_slug>/', views.show_fav_place, name='show_fav_place'),
             ]

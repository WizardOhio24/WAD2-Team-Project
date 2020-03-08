from django.urls import path
from WeatherSTUFF import views

app_name = 'WeatherSTUFF'

urlpatterns = [ path('', views.index, name='index'),
                path('about/', views.about, name='about'),
                path('login/', views.sign_in, name='login'),
                path('register/', views.sign_up, name='register'),
                path('login/myaccount/', views.my_account, name='myaccount'),
                path('login/myaccount/changedetails/', views.change_details, name='changedetails'),
                path('logout/', views.user_logout, name = 'logout'),
                path('add_pin/', views.add_pin, name='add_pin'),
                path('get_pins/', views.get_pins, name='get_pins'),
             ]

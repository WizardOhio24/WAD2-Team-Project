from django.urls import path 
from WeatherSTUFF import views

app_name = 'WeatherSTUFF'

urlpatterns = [ path('', views.index, name='index'),
                path('about/', views.about, name='about'),
                path('login/', views.sign_in, name='login'),
                path('register/', views.sign_up, name='register'),
                path('login/myaccount/', views.my_account, name='myaccount'),
                path('login/myaccount/changedetails/', views.change_details, name='changedetails'),
             ]
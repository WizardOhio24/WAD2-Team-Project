from django.contrib import admin
from WeatherSTUFF.models import UserProfile, Pin

# Register your models here.

class PinAdmin(admin.ModelAdmin):
    list_display = ('title', 'rating', 'num_ratings')

admin.site.register(UserProfile)
admin.site.register(Pin, PinAdmin)
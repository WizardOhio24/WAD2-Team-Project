from django.db import models
from django.contrib.auth.models import User, BaseUserManager
from django.template.defaultfilters import slugify
from django.db.models.signals import pre_save, post_save
import re
import random

class UserProfileManager(models.Manager):
    def get_by_natural_key(self, user):
        return self.get(user=user)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profile_images", blank=True)

    objects = UserProfileManager()

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'UserProfiles'
        unique_together = [['user']]

    def __str__(self):
        print("Username:" + self.user.username)
        return self.user.username

    def natural_key(self):
        return (self.user.username)

#    def value_to_string(self, obj):
#        value = self.value_from_object(obj)
#        return self.get_prep_value(value)

class FavouritePlace(models.Model):
    PLACE_NAME_MAX_LENGTH = 200

    place_name = models.CharField(max_length=PLACE_NAME_MAX_LENGTH)
    x_val = models.FloatField()
    y_val = models.FloatField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        super(FavouritePlace, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.place_name) + "-" + str(self.id)
            self.save()

    def __str__(self):
        return self.place_name

class Pin(models.Model):
    TITLE_MAX_LENGTH = 128
    CONTENT_MAX_LENGTH = 200

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateTimeField()
    rating = models.IntegerField(default=0)
    num_ratings = models.IntegerField(default=0)
    x_val = models.FloatField()
    y_val = models.FloatField()

    slug = models.SlugField()

    title = models.TextField(max_length=TITLE_MAX_LENGTH)
    content = models.TextField(max_length=CONTENT_MAX_LENGTH)

    def save(self, *args, **kwargs):
        if self.num_ratings < 0:
            self.num_ratings = 0

        self.slug = slugify(self.id)
        super(Pin, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    #def natural_key(self):
    #    return self.user.username

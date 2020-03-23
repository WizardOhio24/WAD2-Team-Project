from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify



# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fav_places = models.TextField(blank = True)
    profile_picture = models.ImageField(upload_to="profile_images", blank=True)
    
    class Meta:
        verbose_name_plural = 'UserProfiles'

    def __str__(self):
        return self.user.username


class Pin(models.Model):
    TITLE_MAX_LENGTH = 128
    CONTENT_MAX_LENGTH = 200

    # Currently set to delete pins if user deletes profile, maybe change to "deleted account"
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
        self.slug = slugify(self.title)
        super(Pin, self).save(*args, **kwargs)


    def __str__(self):
        return self.title

    
   

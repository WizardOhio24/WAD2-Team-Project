from django.db import models

# Create your models here.
class User_Profile(models.Model):
    username = models.CharField(max_length=50, unique=True)

    email = models.EmailField()
    fav_places = models.TextField()
    profile_picture = models.ImageField(upload_to="profile_images", blank=True)

    class Meta:
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return self.username


class Pin(models.Model):
    TITLE_MAX_LENGTH = 128
    CONTENT_MAX_LENGTH = 200

    # Currently set to delete pins if user deletes profile, maybe change to "deleted account"
    user = models.ForeignKey(User_Profile, on_delete=models.CASCADE)
    date = models.DateTimeField()
    rating = models.IntegerField(default=0)
    num_ratings = models.IntegerField(default=0)
    x_val = models.FloatField()
    y_val = models.FloatField()

    title = models.TextField(max_length=TITLE_MAX_LENGTH)
    content = models.TextField(max_length=CONTENT_MAX_LENGTH)

    def __str__(self):
        return self.title + "; pin_id=" + id
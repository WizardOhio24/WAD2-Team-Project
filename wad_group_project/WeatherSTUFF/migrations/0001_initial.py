# Generated by Django 2.2.3 on 2020-03-06 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User_Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('fav_places', models.TextField()),
                ('profile_picture', models.ImageField(blank=True, upload_to='profile_images')),
            ],
        ),
        migrations.CreateModel(
            name='Pin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('rating', models.IntegerField(default=0)),
                ('num_ratings', models.IntegerField(default=0)),
                ('x_val', models.FloatField()),
                ('y_val', models.FloatField()),
                ('title', models.TextField(max_length=128)),
                ('content', models.TextField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WeatherSTUFF.User_Profile')),
            ],
        ),
    ]

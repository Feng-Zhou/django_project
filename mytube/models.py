from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from embed_video.fields import EmbedVideoField

class Genre(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    genre = models.ForeignKey(Genre)
    title = models.CharField(max_length=128)
    # year = models.DateTimeField(datetime.year)
    pg = models.IntegerField()
    video = EmbedVideoField(default='')
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    def __str__(self):
        return self.user.username
from msilib import schema
from django.db import models

# Create your models here.
class Movie(models.Model):
    movieId = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'admin\".\"movie_names'

class Rating(models.Model):
    movieId = models.IntegerField(primary_key=True)
    userId = models.IntegerField()
    rating = models.FloatField()
    timestamp = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'admin\".\"movie_ratings'
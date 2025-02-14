from django.db import models

# Create your models here.
class Artists(models.Model):
    GENDER_CHOICES = [
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other')
    ]
    name = models.CharField(max_length=255)
    dob = models.DateTimeField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.CharField(max_length=255)
    first_release_year = models.CharField(max_length=4)
    no_of_albums_released = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'artist'
        verbose_name_plural = 'artists'


class Music(models.Model):
    GENRE_CHOICES = [
        ('rnb', 'rnb'),
        ('co', 'country'),
        ('c', 'classic'),
        ('r', 'rock'),
        ('j', 'jazz'),
    ]
    artist_id = models.IntegerField()
    title = models.CharField(max_length=255)
    album_name = models.CharField(max_length=255)
    genre = models.CharField(max_length=5, choices=GENRE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
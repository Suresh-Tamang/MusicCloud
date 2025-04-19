
from django.db import models
from django.contrib.auth.models import User

class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='artist_profiles/')

class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    release_date = models.DateField()
    cover_art = models.ImageField(upload_to='album_covers/')

class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True)
    genre = models.CharField(max_length=100)
    cover_art = models.ImageField(upload_to='song_covers/')
    audio_file = models.FileField(upload_to='songs/')
    duration = models.DurationField()
    upload_date = models.DateTimeField(auto_now_add=True)
    
class Playlist(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    songs = models.ManyToManyField(Song)
    created_at = models.DateTimeField(auto_now_add=True)
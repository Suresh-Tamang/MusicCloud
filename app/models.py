
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from mutagen import File  # Import the mutagen library
from mutagen.mp3 import MP3  # Import specific format if needed
from django.core.exceptions import ValidationError

class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='artist_profiles/')
    def __str__(self):
        return self.user.username

class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    release_date = models.DateField()
    cover_art = models.ImageField(upload_to='album_covers/')
    def __str__(self):
        return self.title

class Genre(models.Model):
    title = models.CharField(max_length=200)
    info = models.TextField()
    def __str__(self):
        return self.title
    

class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE)
    album = models.ForeignKey('Album', on_delete=models.SET_NULL, null=True, blank=True)
    genre = models.ForeignKey('Genre', on_delete=models.SET_NULL, null=True, blank=True)
    cover_art = models.ImageField(upload_to='song_covers/')
    audio_file = models.FileField(upload_to='songs/')
    duration = models.DurationField(null=True, blank=True)  # Allow null initially
    upload_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calculate the duration of the audio file
        if self.audio_file:
            audio = File(self.audio_file)
            if audio is not None:
                self.duration = audio.info.length  # Get the duration in seconds
                self.duration = timedelta(seconds=self.duration)  # Convert to timedelta

        super().save(*args, **kwargs)  # Call the original save method
    def __str__(self):
        return self.title
class Playlist(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    songs = models.ManyToManyField(Song)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
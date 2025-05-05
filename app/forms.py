from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Artist, Album, Song, Playlist
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

class CustomSignupForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists. ")
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already in use. ")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match. ")
        
        
#artist form
class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['bio','profile_picture']

#Album form
class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title','artist','release_date','cover_art']
    
class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist', 'album', 'genre', 'cover_art', 'audio_file', 'duration']

    def __init__(self, *args, **kwargs):
        super(SongForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-6 mb-3'),
                Column('duration', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('artist', css_class='form-group col-md-4 mb-3'),
                Column('album', css_class='form-group col-md-4 mb-3'),
                Column('genre', css_class='form-group col-md-4 mb-3'),
            ),
            Row(
                Column('cover_art', css_class='form-group col-md-6 mb-3'),
                Column('audio_file', css_class='form-group col-md-6 mb-3'),
            ),
            Submit('submit', 'Save Song')
        )
 
        
        
# Playlist form
class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['title','songs']
    def __init__(self, *args, **kwargs):
        super(PlaylistForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-6 mb-3'),
                Column('songs', css_class='form-group col-md-6 mb-3'),
            ),
            Submit('submit', 'Save Song')
        )
        
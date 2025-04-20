from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Artist, Album, Song, Playlist
from .forms import ArtistForm, AlbumForm, SongForm, PlaylistForm, CustomSignupForm

# Create your views here.
def index(request):
    songs = Song.objects.all().select_related('artist', 'album', 'genre')
    context = {'songs': songs}
    return render(request, 'app/index.html', context)

def exploreStations(request):
    return render(request,'app/explore_stations.html')

def my_stations(request):
    return render(request,'app/my_stations.html')

def audio_player_frame(request):
    return render(request, 'app/audio_frame.html')

def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email = form.cleaned_data['email'],
                password = form.cleaned_data['password']
            )
            login(request,user)
            messages.success(request, "Account created and logged in!")
            return redirect('home')
    else:
        form = CustomSignupForm()
    return render(request, 'app/signup.html', {'form':form})

def login_view(request):
    if request.method =='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            #get the user using email
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request, "Invalid Credentials.")
        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")
    return render(request,'app/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
def dashboard(request):
    user = request.user
    return render(request, 'app/dashboard.html',{
        'username':user.username,
        'email':user.email
    })
    
    
# CRUD
# Insert or Edit Artist( Artist is tied to a user)
@login_required
def artist_create_or_update(request):
    try:
        artist = request.user.artist
    except Artist.DoesNotExist:
        artist = None
        
    form = ArtistForm(request.POST or None, request.FILES or None, instance=artist)
    if form.is_valid():
        artist = form.save(commit=False)
        artist.user = request.user
        artist.save()
        messages.success(request, "Profile saved. ")
        return redirect('artist_detail')
    return render(request, 'artist/artist_form.html',{'form':form})

    
@login_required
def artist_detail(request):
    artist = get_object_or_404(Artist, user = request.user)
    return render(request, 'artist/artist_detail.html',{'artist':artist})

    
# Create Album
@login_required
def album_create(request):
    artist = get_object_or_404(Artist, user=request.user)
    form = AlbumForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        album = form.save(commit=False)
        album.artist = artist
        album.save()
        messages.success(request, "Album added.")
        return redirect('album_list')
    return render(request, 'album/album_form.html',{'form':form})


# List Albums of logged-in user
@login_required 
def album_list(request):
    albums = Album.objects.filter(artist__user=request.user)
    return render(request, 'album/album_list.html',{'album':albums})

@login_required
def album_edit(request, pk):
    album=  get_object_or_404(Album, pk=pk, artist__user=request.user)
    form = AlbumForm(request.POST or None, request.FILES or None, instance=album)
    if form.is_valid():
        form.save()
        messages.success(request, "Album Updated. ")
        return redirect('album_list')
    return render(request, 'album/album_form.html', {'form':form})

@login_required
def album_delete(request,pk):
    album=get_object_or_404(Album,pk=pk, artist__user=request.user)
    album.delete()
    messages.success(request,"Album deleted. ")
    return redirect('album/album_list')

# CRUD for songs
def song_create(request):
    artist = get_object_or_404(Artist, user=request.user)
    form=SongForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        song=form.save(commit=False)
        song.artist = artist
        song.save()
        form.save_m2m()
        messages.success(request,"Song Uploaded .")
        return redirect('song_list')
    return render(request,'songs/song_form.html',{'form':form})

@login_required
def song_list(request):
    songs = Song.objects.filter(artist__user=request.user)
    return render(request,'songs/song_list.html',{'songs':songs})

@login_required
def song_edit(request,pk):
    song = get_object_or_404(Song,pk=pk, artist__user = request.user)
    form = SongForm(request.POST or None, request.FILES or None, instance=song)
    if form.is_valid():
        form.save()
        messages.success(request,"Song Updated")
        return redirect('song_list')
    return render(request,'songs/song_form.html',{'form':form})

@login_required
def song_delete(request,pk):
    song = get_object_or_404(Song,pk=pk,artist__user = request.user)
    song.delete()
    messages.success(request,"Song deleted.")
    return redirect('song_list')


# CRUD   FOR PLAYLISTS  
@login_required
def playlist_create(request):
    form = PlaylistForm(request.POST or None)
    form.fields['songs'].query = Song.objects.filter()
    if form.is_valid():
        playlist = form.save(commit=False)
        playlist.user = request.user
        playlist.save()
        form.save_m2m()
        messages.success(request,"Playlist created.")
        return redirect('playlist_list')
    return redirect(request,'playlist/playlist_form.html',{'form':form})

@login_required
def playlist_list(request):
    playlists=Playlist.objects.filter(user=request.user)
    return render(request,'playlist/playlist_list.html',{'playlists':playlists})

@login_required
def playlist_edit(request,pk):
    playlist=get_object_or_404(Playlist, pk=pk, user=request.user)
    form = PlaylistForm(request.POST or None, instance=playlist)
    form.fields['songs'].queryset=Song.objects.filter(artist__user = request.user)
    if form.is_valid():
        form.save()
        messages.success(request,"Playlist updated. ")
        return redirect('playlist_list')
    return render(request,'playlist/playlist_form.html',{'form':form})

@login_required
def playlist_delete(request,pk):
    playlist=get_object_or_404(Playlist, pk=pk,user=request.user)
    playlist.delete()
    messages.success(request,"Playlist deleted.")
    return redirect('playlist/playlist_list')
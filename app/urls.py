from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
    path('',views.index, name='home'),
     path('persistent-audio/', views.audio_player_frame, name='audio_player_frame'),
    path('explore-stations/', views.exploreStations, name='explore-stations'),
    path('my-stations/', views.my_stations, name='my-stations'),
    path('signup/',views.signup_view, name='signup'),
    path('login/',views.login_view, name='login'),
    path('logout/',views.login_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('artist/', views.artist_create_or_update, name='artist_create_or_update'),
    path('artist/profile/',views.artist_detail,name='artist_detail'),
    
    path('albums/', views.album_list, name='album_list'),
    path('albums/create/', views.album_create, name='album_create'),
    path('albums/edit/<int:pk>/',views.album_edit, name='album_edit'),
    path('albums/delete/<int:pk>/',views.album_delete, name='album_delete'),
    
    path('songs/',views.song_list,name='song_list'),
    path('songs/create/',views.song_create, name='song_create'),
    path('songs/edit/<int:pk>/',views.song_edit, name='song_edit'),
    path('songs/delete/<int:pk>/', views.song_delete, name='song_delete'),
    
    
    path('playlists/',views.playlist_list,name='playlist_list'),
    path('playlists/create/',views.playlist_create, name='playlist_create'),
    path('playlists/edit/<int:pk>/',views.playlist_edit, name='playlist_update'),
    path('playlists/delete/<int:pk>/', views.playlist_delete, name='playlist_delete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path
from . import views
urlpatterns = [
    path('',views.index, name='home'),
    path('explore-stations/', views.exploreStations, name='explore-stations'),
    path('my-stations/', views.my_stations, name='my-stations'),
    path('signup/',views.signup_view, name='signup'),
    path('login/',views.login_view, name='login'),
    path('logout/',views.login_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]

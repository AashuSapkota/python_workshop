from django.urls import path
from . import views

app_name = 'artists'

urlpatterns = [
    # url for artists
    path('', views.ListArtistsAPI.as_view(), name='list_artist'),
    path('artist/new/', views.RegisterArtistAPI.as_view(), name='register_artist'),
    path('artist/<int:artist_id>/edit/', views.UpdateArtistAPI.as_view(), name='update_artist'),
    path('artist/<int:artist_id>/delete/', views.DeleteArtistAPI.as_view(), name='delete_artist'),

    # url for music
    path('music/list/<int:artist_id>/', views.ListArtistMusicAPI.as_view(), name='list_artist_music'),
    path('music/register/<int:artist_id>/', views.RegisterMusicAPI.as_view(), name='register_artist_music'),
    path('music/update/<int:music_id>/', views.UpdateArtistMusicAPI.as_view(), name='update_artist_music'),
    path('music/delete/<int:music_id>/', views.DeleteArtistMusicAPI.as_view(), name='delete_artist_music'),
]

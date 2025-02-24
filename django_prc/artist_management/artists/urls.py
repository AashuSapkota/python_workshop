from django.urls import path
from . import views

app_name = 'artists'

urlpatterns = [
    path('', views.ListArtistsAPI.as_view(), name='list_artist'),
    path('artist/new/', views.RegisterArtistAPI.as_view(), name='register_artist'),
    path('artist/<int:artist_id>/edit/', views.UpdateArtistAPI.as_view(), name='update_artist'),
    path('artist/<int:artist_id>/delete/', views.DeleteArtistAPI.as_view(), name='delete_artist'),
]

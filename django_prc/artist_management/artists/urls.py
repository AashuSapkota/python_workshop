from django.urls import path
from . import views
from django.conf.urls import handler404

# handler404 = views.custom_page_not_found

urlpatterns = [
    path('', views.ListArtistsAPI.as_view(), name='artist_list'),
    path('artist/new/', views.RegisterArtistAPI.as_view(), name='artist_create'),
    path('artist/<int:pk>/edit/', views.UpdateArtistAPI.as_view(), name='artist_update'),
    path('artist/<int:pk>/delete/', views.DeleteArtistAPI.as_view(), name='artist_delete'),

    path('artist/new_web/', views.artist_create, name='artist_create_2'),
    path('artist/list/', views.artist_list, name='artist_list_2'),
    path('artist/<int:pk>/', views.artist_detail, name='artist_detail'),
]

from django.urls import path
from . import views
from django.conf.urls import handler404

handler404 = views.custom_page_not_found

urlpatterns = [
    path('', views.artist_list, name='artist_list'),
    path('artist/<int:pk>/', views.artist_detail, name='artist_detail'),
    path('artist/new/', views.artist_create, name='artist_create'),
    path('artist/<int:pk>/edit/', views.artist_update, name='artist_update'),
    path('artist/<int:pk>/delete/', views.artist_delete, name='artist_delete'),
]

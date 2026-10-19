from django.urls import path
from . import views

app_name = "player"

urlpatterns = [
    path("api/search/", views.search_api, name="search_api"),
    path("playlists/new/", views.playlist_edit, name="playlist_create"),
    path("playlists/<int:pk>/", views.playlist_detail, name="playlist_detail"),
    path("playlists/<int:pk>/edit/", views.playlist_edit, name="playlist_edit"),
    path("playlists/<int:pk>/delete/", views.playlist_delete, name="playlist_delete"),
    path("playlists/<int:pk>/add/", views.playlist_add_track, name="playlist_add"),
    path("playlists/<int:pk>/remove/<int:track_id>/", views.playlist_remove_track, name="playlist_remove"),
]
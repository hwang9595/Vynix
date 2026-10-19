import requests
from django.shortcuts import render

from player import services
from player.models import Playlist


def index(request):
    try:
        popular = services.popular_tracks(12)
    except requests.RequestException:
        popular = []

    playlists = []
    if request.user.is_authenticated:
        playlists = Playlist.objects.filter(owner=request.user)

    return render(request, "home/index.html", {
        "popular": popular,
        "playlists": playlists,
    })
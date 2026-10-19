from django.shortcuts import render

import json

import requests
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from . import services
from .forms import PlaylistForm
from .models import Playlist, Track


def search_api(request):
    """Отдаёт JSON. Его вызывает JavaScript, а не браузер напрямую."""
    q = request.GET.get("q", "").strip()
    if len(q) < 2:
        return JsonResponse({"results": []})
    try:
        results = services.search_tracks(q)
    except requests.RequestException:
        return JsonResponse({"error": "Сервис музыки недоступен"}, status=502)
    return JsonResponse({"results": results})


def playlist_detail(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk)
    is_owner = request.user.is_authenticated and playlist.owner_id == request.user.id
    return render(request, "player/playlist_detail.html", {
        "playlist": playlist,
        "tracks": playlist.tracks.all(),
        "is_owner": is_owner,
    })


@login_required
def playlist_edit(request, pk=None):
    """Одна view на создание (pk=None) и редактирование карточки."""
    playlist = get_object_or_404(Playlist, pk=pk, owner=request.user) if pk else None
    form = PlaylistForm(request.POST or None, instance=playlist)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)     # пока не пишем в базу
        obj.owner = request.user          # владелец берётся из сессии
        obj.save()
        return redirect("player:playlist_detail", pk=obj.pk)
    return render(request, "player/playlist_form.html", {
        "form": form,
        "playlist": playlist,
    })


@login_required
@require_POST
def playlist_delete(request, pk):
    get_object_or_404(Playlist, pk=pk, owner=request.user).delete()
    return redirect("home:index")


@login_required
@require_POST
def playlist_add_track(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk, owner=request.user)
    data = json.loads(request.body)
    track, _ = Track.objects.get_or_create(
        jamendo_id=data["id"],
        defaults={
            "title": data["title"],
            "artist": data["artist"],
            "album": data.get("album", ""),
            "cover": data.get("cover", ""),
            "audio_url": data["audio"],
            "duration": int(data.get("duration") or 0),
        },
    )
    playlist.tracks.add(track)
    return JsonResponse({"ok": True})


@login_required
@require_POST
def playlist_remove_track(request, pk, track_id):
    playlist = get_object_or_404(Playlist, pk=pk, owner=request.user)
    playlist.tracks.remove(track_id)
    return redirect("player:playlist_detail", pk=pk)

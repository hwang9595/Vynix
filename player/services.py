import requests
from django.conf import settings

BASE_URL = "https://api.jamendo.com/v3.0"


def _get(endpoint, **params):
    """Один общий запрос к Jamendo. Добавляет ключ и формат сам."""
    params["client_id"] = settings.JAMENDO_CLIENT_ID
    params["format"] = "json"
    response = requests.get(f"{BASE_URL}/{endpoint}/", params=params, timeout=10)
    response.raise_for_status()          # 4xx/5xx превращаем в исключение
    return response.json().get("results", [])


def _normalize(t):
    """Приводим ответ Jamendo к нашему единому виду."""
    return {
        "id": str(t["id"]),
        "title": t.get("name", ""),
        "artist": t.get("artist_name", ""),
        "album": t.get("album_name", ""),
        "cover": t.get("image", ""),
        "audio": t.get("audio", ""),
        "duration": int(t.get("duration") or 0),
    }


def search_tracks(query, limit=20):
    results = _get("tracks", search=query, limit=limit, imagesize=200)
    return [_normalize(t) for t in results if t.get("audio")]


def popular_tracks(limit=12):
    results = _get("tracks", order="popularity_week", limit=limit, imagesize=200)
    return [_normalize(t) for t in results if t.get("audio")]
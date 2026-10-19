from django.db import models
from django.conf import settings
from django.db import models


class Track(models.Model):
    jamendo_id = models.CharField("ID в Jamendo", max_length=20, unique=True)
    title = models.CharField("Название", max_length=255)
    artist = models.CharField("Исполнитель", max_length=255)
    album = models.CharField("Альбом", max_length=255, blank=True)
    cover = models.URLField("Обложка", max_length=500, blank=True)
    audio_url = models.URLField("Ссылка на аудио", max_length=500)
    duration = models.PositiveIntegerField("Длительность, сек", default=0)

    def __str__(self):
        return f"{self.artist} — {self.title}"


class Playlist(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="my_playlists",
        null=True, blank=True,
    )
    name = models.CharField("Название", max_length=100)
    description = models.TextField("Описание", blank=True)
    tracks = models.ManyToManyField(Track, blank=True, related_name="playlists")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

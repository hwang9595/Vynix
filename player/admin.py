from django.contrib import admin


from django.contrib import admin
from .models import Track, Playlist


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ("title", "artist", "album", "duration")
    search_fields = ("title", "artist")


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    filter_horizontal = ("tracks",)
# Register your models here.

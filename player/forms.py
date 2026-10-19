from django import forms
from .models import Playlist


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ["name", "description"]
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}
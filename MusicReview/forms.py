from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.forms import inlineformset_factory
from django.contrib.auth.models import User

from .models import Review, Release, Artist, Song
from .widgets import Select2Widget, IntegerTime

class ImageColorForm(forms.Form):
    image = forms.ImageField()

class SearchForm(forms.Form):
    search = forms.CharField()

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["content", "score"]
        widgets = {
            'score': forms.Select(),
        }

class ReleaseForm(forms.ModelForm):
    class Meta:
        model = Release
        fields = ['title', 'cover_art', 'release_type', 'genres', 'is_explicit', 'artists']
        widgets = {'genres': Select2Widget(tags=True), 'artists': Select2Widget()}

class TrackForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'length', 'is_explicit', 'artists']
        widgets = {'artists': Select2Widget(), 'length': IntegerTime() }

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'artist_photo']

class ReleaseSort(forms.Form):
    choices = [("Recently added", "Recently added"), ("Recently reviewed", "Recently reviewed")]
    sort = forms.ChoiceField(choices=choices)
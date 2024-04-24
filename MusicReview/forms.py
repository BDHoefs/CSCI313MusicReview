from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.forms import inlineformset_factory
from django.contrib.auth.models import User

from .models import Review, Release, Artist, Song
from .widgets import Select2Widget

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


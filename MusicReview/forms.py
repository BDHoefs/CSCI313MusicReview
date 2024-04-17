from django import forms

class ImageColorForm(forms.Form):
    image = forms.ImageField()

class SearchForm(forms.Form):
    search = forms.CharField()
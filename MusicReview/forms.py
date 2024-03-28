from django import forms

class ImageColorForm(forms.Form):
    image = forms.ImageField()
from django import forms
from django.forms.widgets import Widget
from django.template.loader import render_to_string

class Select2Widget(Widget):
    template_name = 'widgets/select2.html'

    def __init__(self, attrs=None, choices=(), tags=False, *args, **kwargs):
        self.choices = choices
        self.tags = tags # Enables the user to make arbitrary input which doesn't include predefined options
        super().__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        context = {
            'name': name,
            'attrs': self.build_attrs(attrs) if attrs else None,
            'choices': self.choices,
            'tags': self.tags,
        }
        return render_to_string(self.template_name, context)
    
    def value_from_datadict(self, data, files, name):
        return data.getlist(name)
    
class IntegerTime(Widget):
    template_name = 'widgets/time.html'

    def __init__(self, attrs=None, choices=(), *args, **kwargs):
        self.choices = choices
        super().__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        context = {
            'name': name,
            'attrs': self.build_attrs(attrs) if attrs else None,
            'choices': self.choices,
        }

        return render_to_string(self.template_name, context)
    
    def value_from_datadict(self, data, files, name):
        minutes = int(data.getlist(name + '_minutes')[0])
        seconds = int(data.getlist(name + '_seconds')[0])

        return minutes * 60 + seconds
from dal import autocomplete
from django import forms

from .models import AppBus


class AppBusForm(forms.ModelForm):
    class Meta:
        model = AppBus
        fields = ['stop', 'enabled']
        widgets = {
            'stop': autocomplete.ListSelect2(url="stop-autocomplete"),
        }

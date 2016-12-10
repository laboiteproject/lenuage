from dal import autocomplete
from django import forms

from .models import AppBus


class AppBusForm(forms.ModelForm):
    class Meta:
        model = AppBus
        fields = ['stop', 'stop_name', 'enabled']
        widgets = {
            'stop_name': autocomplete.ListSelect2(url="stop-autocomplete")
        }

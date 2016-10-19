from dal import autocomplete
from django import forms


class BikeModelForm(forms.ModelForm):
    class Meta:
        widgets = {
            'id_station': autocomplete.ListSelect2(url='station-autocomplete', forward=('provider',))
        }

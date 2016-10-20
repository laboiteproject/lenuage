from dal import autocomplete
from django import forms


class BikeModelForm(forms.ModelForm):
    def __init__(self, *args, **kw):
        super(BikeModelForm, self).__init__(*args, **kw)
        if self.instance is not None:
            # Setup choices to display selected station
            self.fields['id_station'].widget.choices = ((self.instance.id_station, self.instance.station),)

    class Meta:
        widgets = {
            'id_station': autocomplete.ListSelect2(url='station-autocomplete', forward=('provider',))
        }

from dal import autocomplete
from django import forms


class BikeModelForm(forms.ModelForm):
    def __init__(self, *args, **kw):
        super(BikeModelForm, self).__init__(*args, **kw)
        if self.instance is not None:
            # Saved instance is loaded, setup choices to display the selected value
            self.fields['id_station'].widget.choices = ((self.instance.id_station, self.instance.station),)

    def validate_unique(self):
        super(BikeModelForm, self).validate_unique()
        if self.errors and 'id_station' in self.data:
            # A station was chosen, reinit choices with it
            self.fields['id_station'].widget.choices = ((self.cleaned_data['id_station'], self.data['station']),)

    class Meta:
        widgets = {
            'id_station': autocomplete.ListSelect2(url='station-autocomplete',
                                                   forward=('provider',),
                                                   attrs={'data-allow-clear': 'false'})
        }

    class Media:
        js = ('js/admin_form.js',)

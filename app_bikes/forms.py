from dal import autocomplete
from django import forms


class BikeModelForm(forms.ModelForm):
    def __init__(self, *args, **kw):
        super(BikeModelForm, self).__init__(*args, **kw)
        if self.instance is not None:
            # Saved instance is loaded, setup choices to display the selected value
            self.fields['id_station'].widget.choices = ((self.instance.id_station, self.instance.station),)

    def validate_unique(self):
        """If the form had an error and a station was chosen, we need to setup the widget choices to the previously selected value for the autocomplete to display it properly"""
        super(BikeModelForm, self).validate_unique()
        if self.errors and 'id_station' in self.data:
            self.fields['id_station'].widget.choices = ((self.cleaned_data['id_station'], self.data['station']),)

    class Meta:
        widgets = {
            'id_station': autocomplete.ListSelect2(url='station-autocomplete',
                                                   forward=('provider',),
                                                   attrs={'data-allow-clear': 'false',
                                                          'data-minimum-input-length': 2})
        }

    class Media:
        js = ('js/admin_form.js',)

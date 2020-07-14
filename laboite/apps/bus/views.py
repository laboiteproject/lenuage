# coding: utf-8
import json

import requests
from dal.autocomplete import Select2ListView
from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from boites.views import AppCreateView, AppUpdateView, AppDeleteView
from .forms import AppBusForm
from .models import AppBus


class AppBusCreateView(AppCreateView):
    model = AppBus
    form_class = AppBusForm


class AppBusUpdateView(AppUpdateView):
    model = AppBus
    form_class = AppBusForm


class AppBusDeleteView(AppDeleteView):
    model = AppBus


class BusStopAutocomplete(Select2ListView):
    def get(self, request, *args, **kwargs):
        directions = []
        if self.q:
            params = {
                'dataset': 'tco-bus-circulation-passages-tr',
                'apikey': settings.STAR_API_KEY,
                'q': self.q
            }
            r = requests.get(settings.STAR_API_BASE_URL, params=params)

            records = list(r.json()['records'])
            for record in records:
                data = {
                    'stop_name': record['fields']['nomarret'],
                    'line_short_name': record['fields']['nomcourtligne'],
                    'destination': record['fields']['destination']
                }
                destination = _('Arrêt {stop_name} (direction {destination})')
                directions.append({'id': record['fields']['idarret'],
                                   'text': destination.format(**data)})
        return HttpResponse(json.dumps({'results': directions}))

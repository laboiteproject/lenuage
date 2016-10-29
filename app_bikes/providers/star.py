# coding: utf-8

import requests
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _L

from . import base
from .. import settings


class StarProvider(base.BaseProvider):
    STAR_API_BASE_URL = 'https://data.explore.star.fr/api/records/1.0/search'

    verbose_name = _L(u'Star - Rennes')

    @classmethod
    def get_stations(cls, query):
        if query.isdigit():
            query = 'nom:{query} OR idstation:{query}'.format(query=query)
        else:
            # Querying idstation with a string value raises an error, we remove this field
            query = 'nom:{}'.format(query)
        req = requests.get(cls.STAR_API_BASE_URL, params={'apikey': settings.STAR_API_KEY,
                                                          'dataset': 'vls-stations-etat-tr',
                                                          'fields': 'idstation,nom',
                                                          'q': query,
                                                          'sort': 'nom',
                                                          'timezone': timezone.get_current_timezone_name()})
        if not req.ok:
            return ()
        data = req.json()
        if not data.get('nhits', 0):
            # No matching data found
            return ()

        return [(item['fields']['idstation'], item['fields']['nom']) for item in data.get('records', [])]

    @classmethod
    def get_station_infos(cls, station_id):
        req = requests.get(cls.STAR_API_BASE_URL, params={'apikey': settings.STAR_API_KEY,
                                                          'dataset': 'vls-stations-etat-tr',
                                                          'fields': 'nom,nombreemplacementsactuels,nombrevelosdisponibles,etat',
                                                          'q': 'idstation:"{}"'.format(station_id),
                                                          'timezone': timezone.get_current_timezone_name()})
        if not req.ok:
            return None
        data = req.json()
        if not data.get('nhits', 0):
            # No matching data found
            return None
        data = data['records'][0]['fields']
        return {
            'station': data['nom'],
            'slots': data['nombreemplacementsactuels'],
            'bikes': data['nombrevelosdisponibles'],
            'status': data['etat'] == u'En fonctionnement'
        }
